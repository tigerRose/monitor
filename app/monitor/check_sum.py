#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utility import my_bin, my_hex

class CheckSum(object):
    def __init__(self, data, check_method='crc16'):
        # self.data = data.split()
        self.data = map(lambda x:int(x,16), data)
        self.check_method = check_method

    def cal_check(self):
        crc_reg = 0xFFFF
        for d in self.data:
            crc_reg = crc_reg ^ d
            shift_times = 0
            while shift_times < 8:
                last_bit = crc_reg & 0x1
                crc_reg = crc_reg >> 1

                if last_bit != 0:
                    crc_reg = crc_reg ^ 0xA001
                shift_times += 1
        return my_hex(crc_reg, is_reverse=True)

if __name__ == "__main__":
    # check_sum = CheckSum('01 03 00 00 00 01')
    check_sum = CheckSum(['01','03','00','00','00','01'])
    print check_sum.cal_check()
