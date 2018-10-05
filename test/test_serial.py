#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: test_serial.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/10/02 15:46:27
Brief: 
"""

import re
import sys
import time
import string
from serial import Serial

g_time_interval_s = 0.05    # 重发指令时间间隔不要小于50ms

def main():
    with Serial('/dev/ttyUSB0', 38400, timeout=1) as usb_h:
        while True:
            start = time.time()
            res = usb_h.readline()
            res_l = res.split(':')
            if len(res_l) != 2:
                sys.stderr.write("Unknown Response: %s\n" % res)
                continue

            l = res_l[1].split(",")
            if len(l) != 4:
                sys.stderr.write("Unknown Response: %s\n" % res)
                continue

            power = string.atof(l[0])
            left_speed = string.atof(l[1])
            right_speed = string.atof(l[2])
            sonar = string.atof(l[3].strip())

            print('[Power=%f][lspeed=%f][rspeed=%f][Sonar=%f]' % (
                power, left_speed , right_speed, sonar))

            if sonar <= 30:
                cmd = 'RASPI:0.0,0.0\n'
            else:
                cmd = 'RASPI:5.0,45.0\n'

            print("Command: %s" % cmd)
            usb_h.write(cmd)


            time.sleep(g_time_interval_s)     # 间隔不要小于50ms
            print("TimeInterval: %fs" % (time.time() - start))


if __name__ == '__main__':
    main()

# vim: set ts=4 sw=4 sts=4 tw=100: 
