#!/usr/bin/env python # -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: run.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/09/30 21:51:06
Brief: 
"""

import sys
import logging
import getopt
import signal
from Queue import Queue
from threading import Thread

import config
from rpc.client import Client
from utils.driver import Driver
from utils.timer import Timer


g_dl_server_addr = config.DL_SERVER_HOST + ":" + config.DL_SERVER_PORT
g_pc_server_addr = config.PC_SERVER_HOST + ":" + config.PC_SERVER_PORT


def run_singlethread():
    dl_client = Client(g_dl_server_addr)
    pc_client = Client(g_pc_server_addr)

    with Driver(signal_cycle=0, camera_resolution=(32, 32)) as driver_h:
        for state in driver_h:
            speed = config.BASE_SPEED
            angle = 5
            ## car stat
            if state.power is None:     # connect car failed
                logging.info("[RUN] car stat is None...")
                continue

            ## request DLServer
            pc_client.send(state.image_str)

            response = dl_client.send(state.image_str)
            if response is None:     # connect DLServer failed
                logging.info("[RUN] dl_client rpc failed...")
                continue

            ## drive
            if state.sonar <= 20:
                speed = 0
            angle = response.logid

            driver_h.drive(angle=angle * 9.0, speed=8.0)


class CarStateWorker(Thread):
    """ Get State from car.
    """
    _exit_flag = False

    def __init__(self, driver_h, state_q):
        super(CarStateWorker, self).__init__()
        self.driver_h = driver_h
        self.state_q = state_q

    @staticmethod
    def exit():
        CarStateWorker._exit_flag = True

    def run(self):
        for state in self.driver_h:
            if state.power is None:     # connect car failed
                logging.info("[RUN] car stat is None...")
                continue

            try:
                self.state_q.put(state, block=False)
            except Queue.Full:
                logging.fatal("[RUN] state_q is full...")
                break

            if CarStateWorker._exit_flag:
                break


class CarCtlWorker(Thread):
    """ Send Image to DLServer and Get cmds to control the car.
    """
    _queue_timeout = 0.1
    _exit_flag = False

    def __init__(self, driver_h, state_q, dl_client, pc_client):
        super(CarCtlWorker, self).__init__()
        self.driver_h = driver_h
        self.state_q = state_q
        self.dl_client = dl_client
        self.pc_client = pc_client

    @staticmethod
    def exit():
        CarCtlWorker._exit_flag = True

    def run(self):
        while True:
            try:
                state = self.state_q.get(timeout=_queue_timeout)
            except Queue.Empty:
                logging.info("[RUN] state_q is empty.")
                if CarCtlWorker._exit_flag:
                    break
                continue

            #self.pc_client.send(state.image_str)
            response = self.dl_client.send(state.image_str)
            if response is None:     # connect DLServer failed
                logging.info("[RUN] dl_client rpc failed...")
                continue

            if state.sonar <= 20:
                speed = 0
            angle = response.logid

            self.driver_h.drive(angle=angle * 9.0, speed=8.0)


def stop_worker(signum, frame):
    frame.f_globals['CarStateWorker'].exit()
    frame.f_globals['CarCtlWorker'].exit()
 

def run_multithread():
    ## for exit
    signal.signal(signal.SIGINT, stop_worker)
    signal.signal(signal.SIGTERM, stop_worker)

    with Driver(signal_cycle=0, camera_resolution=(32, 32)) as driver_h:
        dl_client = Client(g_dl_server_addr)
        pc_client = Client(g_pc_server_addr)
        state_q = Queue()      # for car state info
        # worker
        car_state_worker = CarStateWorker(driver_h, state_q)
        car_ctl_worker = CarCtlWorker(driver_h, state_q, dl_client, pc_client)

        car_state_worker.start()
        car_ctl_worker.start()

        car_state_worker.join()
        car_ctl_worker.join()


def usage():
    print "Usage: $0 -t [0/1]"
    print "    -t: if run in multithread."
    exit(0)


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ht:', ['help'])
    except:
        usage()

    is_multi_thread = None

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        if opt == '-t':
            if val in ('0', '1'):
                is_multi_thread = int(val)
            else:
                usage()

    if is_multi_thread is None:
        usage()

    if is_multi_thread:
        run_multithread()
    else:
        run_singlethread()


# vim: set ts=4 sw=4 sts=4 tw=100:
