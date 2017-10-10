#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import socket

from check_sum import CheckSum
from utility import my_hex

__all__ = ["Modbus"]

class Modbus(object):
    name = "Modbus"

    def __init__(self):
        self.bufsize = 1024
        self.is_connect = False
        self.re_connect_times = 3
        self.timeout = 0.5


        self.conn = None

    def init(self, host, port):
        print 'in init %s %s' % (host, port)
        self.addr = (host, port)
        self.connection()
        self.conn.settimeout(self.timeout)

    def connection(self):
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect(self.addr)
        except Exception as e:
            print "connection failed.", e
            self.is_connect = False
            return False
        self.is_connect = True
        return True

    def get(self, addr, command, cmd_param, cmd_length):
        print 'in get %s %s %s %s' % (addr, command, cmd_param, cmd_length)
        # connection to server
        if not self.is_connect:
            times = self.re_connect_times
            while times > 0:
                if self.connection():
                    break
                times -= 1

        if not self.is_connect:
            return None

        # pack the send data
        send_data = []
        send_data.append(addr)
        send_data.append(command)
        send_data.append(cmd_param[:2])
        send_data.append(cmd_param[2:])
        send_data.append("00")
        send_data.append(cmd_length)

        for i in xrange(len(send_data)):
            d = send_data[i]
            if len(d) == 1:
                send_data[i] = '0'+d
            elif len(d) != 2:
                send_data[i] = d[:2]

        # add check sum
        send_check_sum = CheckSum(send_data)
        check_sum_value = send_check_sum.cal_check()
        send_data.extend([check_sum_value[:2], check_sum_value[2:]])

        print 'send: ', ' '.join(send_data)

        send_data = self.pack(send_data)
        # send data
        try:
            self.conn.send(send_data)

            recv_data = self.conn.recv(self.bufsize)
        except Exception as e:
            print "send or recv data failed.", e
            return None

        if recv_data:
            recv_data = self.unpack(recv_data)
            print 'recv: ', ' '.join(recv_data)

            start_pos = 2
            raw_data_str = ''
            for i in xrange(1, int(recv_data[start_pos])+1):
                raw_data_str += recv_data[start_pos+i]

            return self.cal_value(raw_data_str) 

        return None
        #return random.randint(100,300)

    def cal_value(self, s):
        value = 0
        for idx,v in enumerate(s[::-1]):
            value += int(v, 16) * 16**idx
        return value

    def pack(self, d):
        return ''.join(d).decode('hex')

    def unpack(self, d):
        return map(lambda x:x.encode('hex').upper(), d)

    def transformAnalog(self, value, ratio, value_type, precision, min_value, max_value):
        print "in transformAnalog"
        rtn_value = value
        status = '正常'

        try:
            ratio = float(ratio)
        except:
            pass
        else:
            rtn_value *= ratio

        if value_type == 'float':
            rtn_value = float(rtn_value)
            if int(precision) >= 0:
                rtn_value = round(rtn_value, int(precision))
        elif value_type == 'int':
            rtn_value = int(rtn_value)

        if rtn_value > max_value or rtn_value < min_value:
            status = '告警'
        
        return rtn_value, status

    def transformDigit(self, value, ratio, mapper):
        print "in transformDigit"
        rtn_value = value
        status = ''

        try:
            ratio = float(ratio)
        except:
            pass
        else:
            rtn_value *= ratio

        rtn_value = int(rtn_value)

        # mapper example
        # 0=开机;1=关机
        d = self.split_mapper(mapper)
        if rtn_value in d:
            status = d[rtn_value]
        else:
            status = '异常数据'

        return rtn_value, status

    def split_mapper(self, mapper):
        datas = mapper.split(';')
        d = {}
        for data in datas:
            if '=' not in data:
                continue
            data = data.split('=')
            try:
                d[int(data[0])] = data[1]
            except:
                pass
        return d

