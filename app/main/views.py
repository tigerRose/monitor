#-*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, jsonify
from . import main
from .forms import NewProjectForm
from ..models import db, ProjectInfo, AnalogInfo, DigitInfo

import json
from flask import request

import os
basedir = os.path.abspath(os.path.dirname(__file__))
import glob
import json

import codecs
import random

app_path = os.path.dirname(basedir)
devices_path = os.path.join(app_path, 'monitor', 'devices')

# this variable is judge if one project exists
# now i let it be False to test new project feature
# it will got from database lately
is_exists_project = False

@main.route('/', methods=['GET', 'POST'])
def index():

    """
    if 'is_exists_project' in request.args:
        is_exists_project = request.args['is_exists_project']
    print 'in / is_exists_project %s' % is_exists_project
    """
    devices = db.session.query(ProjectInfo).all()
    # test display project html
    #devices = {"project_name":"slina", 
    #           "devices":[
    #            {"id":"001", "name": "KT", "spots":[{"name":"temp", "id":"001"},{"name":"humi", "id":"002"}]},
    #            {"id":"002", "name": "UPS", "spots":[{"name":"voltage", "id":"001"},{"name":"current", "id":"002"}]}
    #            ]}

    if devices is None:
        return redirect(url_for('main.new_project'))
    else:
        project_data = {"project_name":"", "devices":[]}
        project_data["project_name"] = devices[0].project_name
        for device in devices:
            curr_dev = {"id":device.device_id, "name":device.device_name, "spots":[]}
            anas = db.session.query(AnalogInfo).filter_by(device_id=device.device_id).all()
            cur_id = 1
            for ana in anas:
                curr_dev["spots"].append({"id":cur_id, "name":ana.name, "unit":ana.unit, "ratio":ana.ratio, "command":ana.command, "cmd_param":ana.cmd_param})
                cur_id += 1
            digs = db.session.query(DigitInfo).filter_by(device_id=device.device_id).all()
            for dig in digs:
                curr_dev["spots"].append({"id":cur_id, "name":dig.name, "unit":"-", "ratio":dig.ratio, "command":dig.command, "cmd_param":dig.cmd_param})
                cur_id += 1
            project_data["devices"].append(curr_dev)

        # print project_data
        return render_template('index.html', project_data=project_data)

@main.route('/create_project')
def create_project():
    args = request.args
    device_id = args['device_id']
    target_file = os.path.join(devices_path, "%s.dev" % device_id)
    if not os.path.exists(target_file):
        return None
    with codecs.open(target_file, "r", "utf-8") as fh_in:
        dev = fh_in.read()
        dev = json.loads(dev)
    data = {"device":{"name":dev["device"]["description"]}, "spots":[]} 
    for spot in dev["spots"]:
        data["spots"].append({"name":spot["name"]})

    # write the devices info into database

    return json.dumps(data)
    #return render_template('index.html', data=data)

@main.route('/get_item', methods=["GET", "POST"])
def get_item():
    devices_files = glob.glob(os.path.join(devices_path, '*.dev'))
    data = []
    for f in devices_files:
        with codecs.open(f, "r", "utf-8") as fh_in:
            dev = fh_in.read()
            # print dev
            dev = json.loads(dev)
        data.append({"id":dev["device"]["id"],"name":dev["device"]["description"]})
    # data = [{"id":"001", "name":"KT054"}, {"id":"002", "name":"UPS002"}]
    print data
    return json.dumps(data)

@main.route('/new_project', methods=["GET", "POST"])
def new_project():
    form = NewProjectForm()
    if form.validate_on_submit():
        device_com = '192.168.0.1_8888'
        project_name = form.project_name.data
        devices_list = form.devices_name.data
        devices = devices_list.strip().strip(';').split(';')
        # read the project info from json, and write in db
        json_data = read_json_info(devices_list)
        # print json_data
        if len(db.session.query(ProjectInfo).all()) > 0:
            db.session.query(ProjectInfo).delete()
        if len(db.session.query(AnalogInfo).all()) > 0:
            db.session.query(AnalogInfo).delete()
        if len(db.session.query(DigitInfo).all()) > 0:
            db.session.query(DigitInfo).delete()

        for device_id in json_data:
            device_info = json_data[device_id]
            project_info = ProjectInfo(device_id=device_id, device_name=device_info['device']['description'], project_name=project_name, device_com=device_com,protocol=device_info['device']['protocol']) 
            db.session.add(project_info)
        db.session.commit()

        # write the device info to db
        for device_id in json_data:
            device_info = json_data[device_id]['spots']
            for spot in device_info:
                if spot['spot_type'] == '1':
                    # analog spot
                    analog_info = AnalogInfo(device_id=device_id,name=spot['name'],unit=spot['unit'],value_type=spot['value_type'],precision=spot['precision'],min_value=spot['range'].split(',')[0],max_value=spot['range'].split(',')[1],ratio=spot['ratio'],command=spot['command'],cmd_param=spot['cmd_param'],cmd_length=spot['cmd_length'])
                    db.session.add(analog_info)
                elif spot['spot_type'] == '2':
                    # digit spot
                    digit_info = DigitInfo(device_id=device_id,name=spot['name'],ratio=spot['ratio'],command=spot['command'],cmd_param=spot['cmd_param'],cmd_length=spot['cmd_length'],mapper=spot['mapper'])
                    db.session.add(digit_info)
        db.session.commit()

        return redirect(url_for('main.index'))
    return render_template('new_project.html', form=form)

    """
    # old function in jquery
    args = request.args
    project_name = args['project_name']
    devices_name = args['devices_name']
    print project_name, devices_name
    return_data = {"return_code": 0}
    return json.dumps(return_data)
    # return render_template('index.html')
    """

def read_json_info(devices):
    devices_files = glob.glob(os.path.join(devices_path, '*.dev'))
    data = {}
    for f in devices_files:
        bname = os.path.basename(f)[:-4]
        if bname not in devices: continue

        with codecs.open(f, "r", "utf-8") as fh_in:
            dev = fh_in.read()
            # print dev
            dev = json.loads(dev)

        data[bname] = dev
    return data

@main.route("/start")
def start():
    import pika

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='command')

    channel.basic_publish(exchange='',
                            routing_key='command',
                            body='start')
    print " [x] send command 'start'"
    connection.close()

    return ''

@main.route("/end")
def end():
    import pika

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='command')

    channel.basic_publish(exchange='',
                            routing_key='command',
                            body='end')
    print " [x] send command 'end'"
    connection.close()

    return ''

@main.route("/reload", methods=["GET", "POST"])
def reload():
    devices = db.session.query(ProjectInfo).all()

    if devices is None:
        return redirect(url_for('main.new_project'))
    else:
        project_data = {"project_name":"", "devices":[]}
        project_data["project_name"] = devices[0].project_name
        for device in devices:
            curr_dev = {"id":device.device_id, "name":device.device_name, "spots":[]}
            anas = db.session.query(AnalogInfo).filter_by(device_id=device.device_id).all()
            cur_id = 1
            for ana in anas:
                curr_dev["spots"].append({"id":cur_id, "name":ana.name, "unit":ana.unit, "ratio":ana.ratio, "command":ana.command, "cmd_param":ana.cmd_param, "value":random.randint(218,223), "status":random.choice(['正常', '告警'])})
                cur_id += 1
            digs = db.session.query(DigitInfo).filter_by(device_id=device.device_id).all()
            for dig in digs:
                curr_dev["spots"].append({"id":cur_id, "name":dig.name, "unit":"-", "ratio":dig.ratio, "command":dig.command, "cmd_param":dig.cmd_param, "value":random.randint(0,2), "status":random.choice(['正常', '告警'])})
                cur_id += 1
            project_data["devices"].append(curr_dev)

        # print project_data
        return jsonify(project_data)
