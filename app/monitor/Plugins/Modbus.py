#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

__all__ = ["Modbus"]

class Modbus(object):
    name = "Modbus"

    def __init__(self):
        pass

    def init(self, host, port):
        print 'in init %s %s' % (host, port)

    def get(self, command, cmd_param, cmd_length):
        print 'in get %s %s %s' % (command, cmd_param, cmd_length)
        return random.randint(100,300)

    def transformAnalog(self, value, ratio, value_type, precision, min_value, max_value):
        print "in transformAnalog"
        return value, random.choice(["正常","告警"])

    def transformDigit(self, value, ratio, mapper):
        print "in transformDigit"
        return value, random.choice(["正常","告警"])

