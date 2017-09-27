from flask import render_template, redirect, url_for
from . import main
from .forms import NewProjectForm
from ..models import db, ProjectInfo

import json
from flask import request

import os
basedir = os.path.abspath(os.path.dirname(__file__))
import glob
import json

import codecs

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
    if is_exists_project:
        return render_template('index.html')
    else:
        #return render_template('new_project.html')
        return redirect(url_for('main.new_project'))

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
        for device_id in json_data:
            device_info = json_data[device_id]
            project_info = ProjectInfo(device_id=device_id, device_name=device_info['device']['description'], project_name=project_name, device_com=device_com, relation_table=device_id+'_relation')
            db.session.add(project_info)
        db.session.commit()

        # display index for a existing project
        global is_exists_project
        is_exists_project = True
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
