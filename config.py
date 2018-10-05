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


# init log
logging.basicConfig(
		level=logging.INFO,
		format='[%(asctime)s][%(levelname)s]%(message)s',
		datefmt='%Y-%m-%d %H:%M:%S',
		filename='./log.run',
		filemode='w')

# vim: set ts=4 sw=4 sts=4 tw=100: 
