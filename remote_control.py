#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: remote_control.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/10/07 15:51:55
Brief: remote control for samples 
"""

import os
import re
import config
from rpc.client import Client
from utils.driver import Driver

g_output = './sample/'
g_non_numeric = re.compile(ur'[^\d]+')

def wheel(label):
    base_angle = 9.0
    return (base_angle * label)


def run():
    client = Client()
    index = 0
    label = 5    # forward

    with Driver(signal_cycle=0, camera_resolution=(320, 240)) as driver_h:

        for driver in driver_h:
            ## info
            if driver.power is None:
                continue
            
            print('[Power=%f][lspeed=%f][rspeed=%f][Sonar=%f]' % (
                        driver.power,
                        driver.left_speed ,
                        driver.right_speed,
                        driver.sonar))
            index += 1
            ## image
            client.send(driver.image_stream.getvalue())

            ## control
            ipt = raw_input("Angle:")
            if re.search(g_non_numeric, ipt):
                print("Illegal Input...")
                continue

            if ipt:
                ipt = int(ipt)
                if ipt > 10:
                    print("Illegal Input...")
                    continue
                label = int(ipt)

            ## save samples
            driver.image.save("%s/%d_%d.png" % (g_output, index, label))

            driver.drive(angle=wheel(label), speed=5.0)


if __name__ == '__main__':
    if not os.path.exists(g_output):
        os.makedirs(g_output)

    run()


# vim: set ts=4 sw=4 sts=4 tw=100: 
