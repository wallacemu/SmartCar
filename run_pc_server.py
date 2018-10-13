#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: server.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/09/30 21:52:56
Brief: Show pictures from car-camera at PC
"""

import time
import logging
import cv2
import numpy
import grpc
from concurrent import futures
from rpc.proto import data_pb2
from rpc.proto import rpc_pb2_grpc

import config


class PCServer(rpc_pb2_grpc.RPCServicer):
    """ Show Images
    """

    def run(self, request, context):
        logging.info("ReceiveImage(%d, %d)" % (
            request.width, request.height))

        data = numpy.fromstring(request.image, dtype=numpy.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow("CarCamera", image)
        cv2.waitKey(1)

        return data_pb2.ResData(0)   # Nothing


def main():
    server_addr = config.LOCAL_HOST + ":" + config.PC_SERVER_PORT

    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(
        max_workers=config.PC_SERVER_THREADS))

    rpc_pb2_grpc.add_RPCServicer_to_server(PCServer(), server)
    server.add_insecure_port(server_addr)
    server.start()

    logging.info("Start PCServer(%s) Successfully..." % server_addr)

    try:
        while True:
            time.sleep(config.ONE_DAY)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    main()

# vim: set ts=4 sw=4 sts=4 tw=100: 
