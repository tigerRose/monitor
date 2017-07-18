#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import serial

ser = serial.Serial('com3', 9600, timeout=0.3)

while True:
    data = ser.readall()
    if len(data) != 0:
        print data
        # ser.write(send_data.decode('hex'))
    sleep(0.3)

