#!/usr/bin/env python # -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: run.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/09/30 21:51:06
Brief: 
"""

import logging

import config
from rpc.client import Client
from utils.driver import Driver
from utils.timer import Timer


def run():
    dl_server_addr = config.DL_SERVER_HOST + ":" + config.DL_SERVER_PORT
    pc_server_addr = config.PC_SERVER_HOST + ":" + config.PC_SERVER_PORT 
    dl_client = Client(dl_server_addr)
    pc_client = Client(pc_server_addr)

    with Driver(signal_cycle=0, camera_resolution=(32, 32)) as driver_h:
        for driver in driver_h:
            speed = config.BASE_SPEED
            angle = 5
            ## car stat
            if driver.power is None:     # connect car failed
                logging.info("[RUN] car stat is None...")
                continue

            ## request DLServer
            pc_client.send(driver.image_stream.getvalue())
            response = dl_client.send(driver.image_stream.getvalue())
            if response is None:     # connect DLServer failed
                logging.info("[RUN] dl_client rpc failed...")
                continue

            ## drive
            if driver.sonar <= 20:
                speed = 0
            angle = response.logid

            driver.drive(angle=angle * 9.0, speed=8.0)


if __name__ == '__main__':
    run()


# vim: set ts=4 sw=4 sts=4 tw=100: 
