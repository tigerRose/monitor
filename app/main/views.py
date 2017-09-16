from flask import render_template
from . import main

import json
from flask import request


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/create_project')
def create_project():
    args = request.args
    device_id = args['device_id']
    if device_id == "001":
        data = {"device":{"name": "KT054"}, "spots":[{"name":"spot1"}, {"name":"spot2"}]}
    elif device_id == "002":
        data = {"device":{"name": "UPS002"}, "spots":[{"name":"spot1"}, {"name":"spot2"}, {"name":"spot3"}]}
    print data
    return json.dumps(data)
    #return render_template('index.html', data=data)

@main.route('/get_item', methods=["GET", "POST"])
def get_item():
    data = [{"id":"001", "name":"KT054"}, {"id":"002", "name":"UPS002"}]
    print data
    return json.dumps(data)

