#-*- coding:utf-8 -*-

import os
import time
import random

import redis

from PluginManager import PluginManager

def start():
    r = redis.Redis(host="127.0.0.1", port=6379, db=0)

    # load the plugins for every device
    plugin_manager = PluginManager()
    plugin_manager.LoadAllPlugin()

    plugins = {}
    for device in r.lrange("devices", 0, -1):
        protocol = r.get("protocol:%s" % device)

        plugin = plugin_manager.GetPluginByName(protocol.title())

        host = r.get("ip:%s" % device)
        port = r.get("port:%s" % device)
        plugin.init(host, port)
        plugins[device] = plugin

    while True:
        print 'in start'
        for device in r.lrange("devices", 0, -1):
            for spot in r.lrange("spots:%s" % device, 0, -1):
                command = r.get("device:%s:spot:%s:%s" % (device, spot[1:], 'command'))
                cmd_param = r.get("device:%s:spot:%s:%s" % (device, spot[1:], 'cmd_param'))
                cmd_length = r.get("device:%s:spot:%s:%s" % (device, spot[1:], 'cmd_length'))
                ratio = r.get("device:%s:spot:%s:%s" % (device, spot[1:], 'ratio'))
                value = plugins[device].get(command, cmd_param, cmd_length)
                if spot[0] == 'A':
                    value_type = r.get("device:%s:spot:%s:%s" % (device, spot[1:], 'value_type'))
                    precision = r.get("device:%s:spot:%s:%s" % (device, spot[1:], 'precision'))
                    min_value = r.get("device:%s:spot:%s:%s" % (device, spot[1:], 'min_value'))
                    max_value = r.get("device:%s:spot:%s:%s" % (device, spot[1:], 'max_value'))

                    value, status = plugins[device].transformAnalog(value, ratio, value_type, precision, min_value, max_value)
                elif spot[0] == 'D':
                    mapper = r.get("device:%s:spot:%s:%s" % (device, spot[1:], 'mapper'))

                    value, status = plugins[device].transformDigit(value, ratio, mapper)

                r.set("device:%s:spot:%s:value" % (device, spot[1:]), value)
                r.set("device:%s:spot:%s:status" % (device, spot[1:]), status)

        time.sleep(5)

    """
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
    """

