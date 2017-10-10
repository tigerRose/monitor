#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import random
import socket

from check_sum import CheckSum
from utility import my_hex

class SimulateModbustcp(object):
    """ This class using for simulate modbus to fake data to return """

    def __init__(self, ip='localhost', port=8888, timeout=3):
        self.ip = ip
        self.port = port
        self.timeout = timeout

        self.recv_len = 8
        self.intervals = 0.1
        self.bufsize = 1024

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip, self.port))
        sock.listen(5)

        recv_data = []
        send_data = []

        while True: 
            client_sock, client_addr = sock.accept()
            while True:
                try:
                    recv_data = client_sock.recv(self.bufsize)
                except Exception as e:
                    print "sock recv error:", e
                    client_sock.close()
                    break
                if not recv_data:
                    sleep(self.intervals)
                    break

                recv_data = map(lambda x: x.encode('hex').upper(), recv_data)
                print 'recv:', ' '.join(recv_data)
                addr, cmd = recv_data[0], recv_data[1]
                recv_len = int(recv_data[4],16) << 8 | int(recv_data[5],16)

                # check the recv data's checksum
                recv_check_sum = CheckSum(recv_data[:-2])
                if recv_check_sum.cal_check() != ''.join(recv_data[-2:]):
                    print "Checksum error for recving data: %s" % ' '.join(recv_data)


                # calculate the return data
                send_data = [addr, cmd]

                if cmd == '01' or cmd == '02':
                    send_len = recv_len/8 if recv_len%8 == 0 else recv_len/8 + 1
                elif cmd == '03' or cmd == '04':
                    send_len = recv_len * 2

                send_data.append(my_hex(send_len, is_reverse=False, l=2))

                faked_data = my_hex(random.randint(0,256), is_reverse=False, l=2)
                send_data.extend([faked_data]*send_len)

                # add crc16 checksum
                send_check_sum = CheckSum(send_data)
                check_sum_value = send_check_sum.cal_check()
                send_data.extend([check_sum_value[:2], check_sum_value[2:]])

                print 'send:', ' '.join(send_data)
                client_sock.send(''.join(send_data).decode('hex'))
        client_sock.close()
        sock.close()
            
    def end(self):
        pass


if __name__ == "__main__":
    simulate_modbustcp = SimulateModbustcp()
    simulate_modbustcp.start()

    
