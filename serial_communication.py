#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial

# s = serial.Serial('com3', 9600, timeout=0.3)
s = serial.Serial('/dev/tty.Bluetooth-Incoming-Port', 9600, timeout=0.3)
send_data = '01 03 00 00 00 01 84 0A'

for i in xrange(3):
    s.write(send_data.replace(' ','').decode('hex'))
    print 'send: %s' % send_data
    recv_data = s.readall()
    print 'recv: %s' % recv_data.encode('hex')
