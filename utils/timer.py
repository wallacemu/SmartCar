#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: timer.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/10/07 14:37:04
Brief: Return the execution time before and after.
"""

import time

class Timer(object):
    """Return the execution time before and after.
    """
    def __init__(self):
        self.start = time.time()

    def elapse(self):
        e_ms = (time.time() - self.start) * 1000 
        self.start = time.time()

        return e_ms


if __name__ == '__main__':
    timer = Timer()
    for i in range(10):
        print "%dms" % timer.elapse()
        time.sleep(0.05)


# vim: set ts=4 sw=4 sts=4 tw=100: 
