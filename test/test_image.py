#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: test_image.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/10/10 22:34:19
Brief: test for image process 
"""

import os
import sys
from PIL import Image


def process(im):
    return im.resize((32, 32), Image.ANTIALIAS)


def local_f(dir_out, dir_in, files):
    for f_in in files: 
        f_path = os.path.join(dir_in, f_in)
        print("Process: " + f_path)

        im = Image.open(f_path)
        im = process(im)

        f_out = f_path
        if dir_out:
            f_out = os.path.join(dir_out, f_in)

        im.save(f_out)
        im.close()


def usage():
    print("Usage: %s -f/-d file/dir [dir_out-dir]" % sys.argv[0])


if __name__ == '__main__':
    if len(sys.argv) != 4 and len(sys.argv) != 3:
        usage()
        exit(0)

    model = sys.argv[1]
    dir_in = sys.argv[2]
    dir_out = None

    if len(sys.argv) == 4:
        dir_out = sys.argv[3]
        if not os.path.isdir(dir_out):
            os.makedirs(dir_out)

    if model == "-f":
        local_f(dir_out, "", [dir_in])
    elif model == "-d":
        os.path.walk(dir_in, local_f, dir_out)
    else:
        usage()


# vim: set ts=4 sw=4 sts=4 tw=100:
