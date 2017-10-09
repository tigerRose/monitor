#-*- coding:utf-8 -*-

import time
import random

import redis

def start():
    r = redis.Redis(host="127.0.0.1", port=6379, db=0)

    while True:
        print 'in start'
        for device in r.lrange("devices", 0, -1):
            for spot in r.lrange("spots:%s" % device, 0, -1):
                if spot[0] == 'A':
                    r.set("device:%s:spot:%s:value" % (device, spot[1:]), random.randint(100,300))
                    r.set("device:%s:spot:%s:status" % (device, spot[1:]), random.choice(["正常","告警"]))
                elif spot[0] == 'D':
                    r.set("device:%s:spot:%s:value" % (device, spot[1:]), random.randint(0,3))
                    r.set("device:%s:spot:%s:status" % (device, spot[1:]), random.choice(["正常","告警"]))

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

