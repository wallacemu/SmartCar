#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: run.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/09/30 21:51:06
Brief: 
"""

import time

import config
from rpc.client import Client
from utils.driver import Driver

def run():
    client = Client()
    with Driver() as driver_h:
        start = time.time()

        for driver in driver_h:
            print("TimeInterval: %fs" % (time.time() - start))

            ## info
            print driver.power, driver.left_speed
            client.send(driver.image_stream.getvalue())

            ## drive
            driver.drive(angle=45.0, speed=5.0)

            start = time.time()


if __name__ == '__main__':
    run()

# vim: set ts=4 sw=4 sts=4 tw=100: 
