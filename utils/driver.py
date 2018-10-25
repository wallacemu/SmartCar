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
import collections
from serial import Serial

from camera import Camera
from timer import Timer

## the states of the car 
CarState = collections.namedtuple('CarState',
        ['power', 'lspeed', 'rspeed', 'sonar', 'image', 'image_str'])


class Driver(object):
    """ To send the command to the Arduino to drive the car;
    """
    _signal_period = 0.05     # signal control cycle
    _baud_rate = 38400       # the baud rate between raspberrypi and Arduino
    _log_cycle = 2           # the cycle for log print

    def __init__(self, signal_period=None, camera_resolution=None):
        if not signal_period is None:
            self._signal_period = signal_period

        self.log_cnt = 0     # count for log-cycle
        self.timer = Timer()
        ## handle
        self.car_h = Serial('/dev/ttyUSB0', self._baud_rate, timeout=1)
        self.camera_h = Camera(resolution=camera_resolution)

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
            states of the car.
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
        lspeed = string.atof(info_l[1])
        rspeed = string.atof(info_l[2])
        sonar = string.atof(info_l[3].strip())

        return (power, lspeed, rspeed, sonar)

    def __iter__(self):
        return self

    def next(self):
        self.log_cnt += 1
        time.sleep(self._signal_period)   # wait a moment for acquisition period
        ## base info
        arduino_info = self.car_h.readline()
        (power, lspeed, rspeed, sonar) = self.__parse__(arduino_info)
        ## camera
        image_str, capture_time = self.camera_h.capture()
        ## log
        if (not power is None) and (self.log_cnt % self._log_cycle == 0):
            logging.info('[Driver][SigCycle=%dms][CaptureTime=%dms]'
                    '[Power=%f][lspeed=%f][rspeed=%f][Sonar=%f]' % (
                        self.timer.elapse() / self._log_cycle,
                        capture_time, power, lspeed , rspeed, sonar))

        return CarState(power, lspeed, rspeed, sonar, None, image_str)

    def drive(self, angle, speed):
        self.car_h.write(
                "RASPI:%f,%f\n" % (speed, angle))

        
# vim: set ts=4 sw=4 sts=4 tw=100: 
