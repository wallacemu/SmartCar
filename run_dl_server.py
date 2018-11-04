#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: run_dlserver.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/10/08 15:42:51
Brief: To run a decision maker.
       Run DLServer in the docker which
       has been installed with paddlepaddle.
"""

import io
import time
import logging
import numpy
import grpc
from PIL import Image
from concurrent import futures

from rpc.proto import data_pb2
from rpc.proto import rpc_pb2_grpc

import config
from DL.predictor import Predictor


class DLServer(rpc_pb2_grpc.RPCServicer):
    """
    DLServer实现类
    """
    def __init__(self, model_dir=None, img_size=None):
        super(DLServer, self).__init__()
        self.predictor = Predictor(model_dir, img_size)

    def run(self, request, context):
        img = Image.open(io.BytesIO(request.image))
        angle = self.predictor.predict(img)

        logging.info("[DLServer] angle=%d" % angle)

        return data_pb2.ResData(angle=angle)


def main():
    server_addr = config.LOCAL_HOST + ":" + config.DL_SERVER_PORT

    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(
        max_workers=config.DL_SERVER_THREADS))

    rpc_pb2_grpc.add_RPCServicer_to_server(DLServer(), server)
    server.add_insecure_port(server_addr)
    server.start()

    logging.info("Start DLServer(%s) Successfully..." % server_addr)

    try:
        while True:
            time.sleep(config.ONE_DAY)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    main()

# vim: set ts=4 sw=4 sts=4 tw=100: 
