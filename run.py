#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: run.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/09/30 21:51:06
Brief: 
"""

import config
from rpc.client import Client
from utils.driver import Driver


g_base_angle = 9.0
g_base_speed = 7.0


def run():
    dl_client = Client(server_addr="192.168.3.3:8001")
    pc_client = Client(server_addr="192.168.3.3:8002")

    with Driver(signal_cycle=0, camera_resolution=(32, 32)) as driver_h:
        for driver in driver_h:
            speed = g_base_speed
            angle = 5
            ## car stat
            if driver.power is None:     # connect car failed
                continue

            ## request DLServer
            pc_client.send(driver.image_stream.getvalue())
            response = dl_client.send(driver.image_stream.getvalue())
            if response is None:     # connect DLServer failed
                continue

            ## drive
            if driver.sonar <= 20:
                speed = 0
            angle = response.logid

            driver.drive(angle=angle * 9.0, speed=8.0)


if __name__ == '__main__':
    run()


# vim: set ts=4 sw=4 sts=4 tw=100: 
