#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import multiprocessing
import subprocess
import signal
import time

import pika
import gevent

from monitor import start

def singleton(cls, *args, **kwargs):
    instances = {}  
    def getinstance():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance

@singleton
class MyGlobal(object):
    def __init__(self):
        self.exists_sub_process = False
        self.sub_process = None

my_global = MyGlobal()

def monitor_run():
    print 'in monitor_run'
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='command')

    def callback(ch, method, properties, body):
        print " [x] received %r" % body
        print "exists_sub_process %s" % my_global.exists_sub_process
        # if body == 'start' and not exists_sub_process:
        if body == 'start' and not my_global.exists_sub_process:
            my_global.exists_sub_process = True
            my_global.sub_process = multiprocessing.Process(target=start)
            my_global.sub_process.start()
        elif body == 'end' and my_global.exists_sub_process:
            my_global.exists_sub_process = False
            if my_global.sub_process is not None:
                os.kill(my_global.sub_process.pid, signal.SIGKILL)
                my_global.sub_process = None
        else:
            pass

    channel.basic_consume(callback,
                            queue='command',
                            no_ack=True)

    channel.start_consuming()


def monitor_test():
    print gevent.getcurrent()
    print 'in monitor_test'
