#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: camera.py
Author: wangsen(wangsen@baidu.com)
Date: 2018/08/14 00:28:15
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

def main():
    client = Client()
    stream = io.BytesIO()

    with PiCamera() as camera:
        #camera.resolution = (640, 480)
        camera.resolution = (320, 240)
        camera.framerate = 10
        camera.hflip = True
        camera.vflip = True
        # warm up the camera
        time.sleep(2)
        #camera.capture("test.png")
        cnt = 0
        for foo in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            client.send(stream.getvalue(), 640, 480)
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
    main()

"""
    rawCapture = PiRGBArray(camera, size=(640, 480)) 

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
"""


# vim: set ts=4 sw=4 sts=4 tw=100: 
