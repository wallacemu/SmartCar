#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: config.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/10/05 22:18:23
Brief: Global Configuration 
"""

import logging

# Global Configure
## Server
LOCAL_HOST = "0.0.0.0"

DL_SERVER_PORT = "8001"
DL_SERVER_HOST = "192.168.3.3"
DL_SERVER_THREADS=1

PC_SERVER_PORT = "8002"
PC_SERVER_HOST = "192.168.3.3"
PC_SERVER_THREADS=1  # 不要多线程，否则imshow会有问题

ONE_DAY=86400

## Camera
IMAGE_SIZE = (32, 32)    # (width, height)

## Control ENV
ANGLE_LIST = [0, 2, 5, 8, 10]
BASE_ANGLE = 9.0
BASE_SPEED = 7

# init log
logging.basicConfig(
		level=logging.INFO,
		format='[%(asctime)s][%(levelname)s]%(message)s',
		datefmt='%Y-%m-%d %H:%M:%S',
		filename='./log.run',
		filemode='w')

# vim: set ts=4 sw=4 sts=4 tw=100: 
