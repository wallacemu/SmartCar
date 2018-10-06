#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: driver.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/10/05 23:34:38
Brief: drive the car
"""

import time
import string
import traceback
import logging
from serial import Serial

from camera import Camera


class Driver(object):
    """ To send the command to the Arduino to drive the car;
    """
    _time_interval = 0.05
    _baud_rate = 38400

    def __init__(self, time_interval=0.05):
        self._time_interval = time_interval
        ## info
        self.power = 0.0
        self.left_speed = 0.0
        self.right_speed = 0.0
        self.sonar = 0.0
        self.image = None
        self.image_stream = None
        ## handle
        self.car_h = Serial('/dev/ttyUSB0', self._baud_rate, timeout=1)
        self.camera_h = Camera()

    def __enter__(self):
        return self

    def __exit__(self, exe_type, exe_val, exe_trace):
        self.car_h.close()
        self.camera_h.exit()

        logging.info("[Driver] close and exit.")
        # 其它错误需要提示
        if exe_trace and exe_type != KeyboardInterrupt:
            logging.info("[Driver] %s" % traceback.format_exc(exe_trace))

        return True  # do nothing

    def __parse__(self, car_state):
        """ Parse the response from the car, which is about the
            state of the car.
        """
        info_l = car_state.split(':')

        if len(info_l) != 2 or info_l[0] != "MCU":
            logging.info("[Driver] Unknown Car State: %s" % car_state)
            return [None] * 4

        info_l = info_l[1].split(",")
        if len(info_l) != 4:
            logging.info("[Driver] Unknown Car State: %s" % car_state)
            return [None] * 4

        power = string.atof(info_l[0])
        left_speed = string.atof(info_l[1])
        right_speed = string.atof(info_l[2])
        sonar = string.atof(info_l[3].strip())

        logging.info('[Driver][Power=%f][lspeed=%f][rspeed=%f]'
            '[Sonar=%f]' % (power, left_speed , right_speed, sonar))

        return (power, left_speed, right_speed, sonar)

    def __iter__(self):
        return self

    def next(self):
        time.sleep(self._time_interval)
        ## car info
        car_state = self.car_h.readline()
        (self.power, self.left_speed, self.right_speed,
                self.sonar) = self.__parse__(car_state)
        ## camera
        self.image_stream, self.image = self.camera_h.capture()

        return self


    def drive(self, angle, speed):
        self.car_h.write(
                "RASPI:%f,%f\n" % (speed, angle))

        
# vim: set ts=4 sw=4 sts=4 tw=100: 