#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: camera.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/10/01 00:11:03
Brief: 
"""

import sys
sys.path.append("..")

import time
import cv2
import io
from picamera.array import PiRGBArray
from picamera import PiCamera
from rpc.client import Client

import config
from utils.timer import Timer


g_img_size = (32, 32)


def capture():
    server_addr = config.PC_SERVER_HOST + ":" + config.PC_SERVER_PORT

    client = Client(server_addr)
    stream = io.BytesIO()

    with PiCamera() as camera:
        camera.resolution = g_img_size
        camera.framerate = 30
        camera.hflip = True
        camera.vflip = True
        # warm up the camera
        time.sleep(2)

        cnt = 0
        cycle_timer = Timer()
        capture_timer = Timer()

        for foo in camera.capture_continuous(stream, format='jpeg',
                use_video_port=True):
            t1 = capture_timer.elapse()
            tmp_timer = Timer()
            client.send(stream.getvalue(), g_img_size[0], g_img_size[1])
            t2 = tmp_timer.elapse()

            cnt += 1
            if cnt >= 1000:
                break

            stream.seek(0)
            stream.truncate()
            t3 = tmp_timer.elapse()

            t4 = cycle_timer.elapse()
            print "cycle:", t4, "capture:", t1, "send:", t2, "clear_stream:", t3
            capture_timer.elapse()


if __name__ == '__main__':
    capture()


# vim: set ts=4 sw=4 sts=4 tw=100: 
