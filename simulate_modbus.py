#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import serial

ser = serial.Serial('/dev/tty.Bluetooth-Incoming-Port', 9600, timeout=0.3)

fh_out = open('out', 'w')
fh_out.write('begin\n')

while True:
    data = ser.readall()
    fh_out.write('recv :%s\n' % data)
    if len(data) != 0:
        send_data = '01 03 02 00 01'
        ser.write(send_data.decode('hex'))
        fh_out.write('send :%s\n' % send_data)
    sleep(0.3)

fh_out.write('end\n')
fh_out.close()
