#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: test_rpc.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/10/02 15:46:27
Brief: test for rpc: upload images to the server
"""

import io
import time
import sys
sys.path.append('../')

from PIL import Image
from rpc.client import Client


def main(files):
    client = Client(server_addr="192.168.3.3:8001")
    stream = io.BytesIO()

    start = time.time()

    for f in files:
        ## clear
        stream.seek(0)
        stream.truncate()
        ## get image
        img = Image.open(f)
        img.save(stream, format="PNG")
        ## send
        res = client.send(stream.getvalue(), img.size[0], img.size[1])
        if res:
            print f, res.logid
    
    print "RPC: request_time=%fms" % ((time.time() - start) / len(files) * 100)
        

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: %s image1 image2..." % sys.argv[0])
        exit(0)

    main(sys.argv[1:])
    
# vim: set ts=4 sw=4 sts=4 tw=100: 
