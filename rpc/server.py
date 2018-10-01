#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: server.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/09/30 21:52:56
Brief: RPC server 
"""

import time
import logging

import cv2
import numpy
import matplotlib.pyplot as plt

import grpc
from proto import data_pb2
from proto import rpc_pb2_grpc
from concurrent import futures


g_server_addr = "192.168.3.3:8801"
g_sleep_time = 86400
g_worker_num = 1  # 调用cv2.imshow就不要多线程，容易卡死


class Server(rpc_pb2_grpc.RPCServicer):
    """
    Server实现类
    """
    _s_cnt = 0

    def run(self, request, context):
        Server._s_cnt += 1

        logging.info("Receive PIC=%d (%d, %d)" % (
            Server._s_cnt, request.width, request.height))

        data = numpy.fromstring(request.image, dtype=numpy.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow("img", image)
        cv2.waitKey(1)

        return data_pb2.ResData(logid=Server._s_cnt)


def main():
    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(
        max_workers=g_worker_num))
    rpc_pb2_grpc.add_RPCServicer_to_server(Server(), server)
    server.add_insecure_port(g_server_addr)
    server.start()

    try:
        while True:
            time.sleep(g_sleep_time)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    main()

# vim: set ts=4 sw=4 sts=4 tw=100: 
