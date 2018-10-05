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


g_img_size = (640, 480)


def capture():
    rawCapture = PiRGBArray(camera, size=g_img_size)

    time.sleep(0.1) # capture frames from the camera

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array # show the frame
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break


def capture_remote():
    client = Client()
    stream = io.BytesIO()

    with PiCamera() as camera:
        camera.resolution = g_img_size
        camera.framerate = 10
        camera.hflip = True
        camera.vflip = True
        # warm up the camera
        time.sleep(2)

        cnt = 0
        for foo in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            client.send(stream.getvalue(), g_img_size[0], g_img_size[1])
            # continuous
            time.sleep(0.05)
            cnt += 1
            if cnt >= 1000:
                break
            # 流定位到最开始，重新写入
            stream.seek(0)
            # 清空当前文件指针之后的内容，即全部stream
            stream.truncate()


if __name__ == '__main__':
    capture_remote()


# vim: set ts=4 sw=4 sts=4 tw=100: 
