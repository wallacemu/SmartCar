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
import time

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
    label = 5    # forward

    with Driver(signal_period=0, camera_resolution=(320, 240), output_im=True) as driver_h:

        for car_state in driver_h:
            ## info
            if car_state.power is None:
                continue
            
            print('[Power=%f][lspeed=%f][rspeed=%f][Sonar=%f]' % (
                        car_state.power,
                        car_state.lspeed ,
                        car_state.rspeed,
                        car_state.sonar))
            ## image
            client.send(car_state.image_str)

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
            index = int(time.time() * 1000)
            car_state.image.save("%s/%d_%d.png" % (g_output, index, label))

            driver_h.drive(angle=wheel(label), speed=5.0)


if __name__ == '__main__':
    if not os.path.exists(g_output):
        os.makedirs(g_output)

    run()


# vim: set ts=4 sw=4 sts=4 tw=100: 
