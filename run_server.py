#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: run_server.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/10/08 15:42:51
Brief: To run a decision maker.
       Run PredictServer in the docker which 
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
from DL.predictor import Predictor

import config

g_server_addr = "0.0.0.0:8001"
g_sleep_time = 86400
g_worker_num = 2 


class PredictServer(rpc_pb2_grpc.RPCServicer):
    """
    PredictServer实现类
    """
    def __init__(self, model_dir=None, img_size=None):
        super(PredictServer, self).__init__()
        self.predictor = Predictor(model_dir, img_size)

    def run(self, request, context):
        img = Image.open(io.BytesIO(request.image))
        angle = self.predictor.predict(img)

        logging.info("[PredictServer] angle=%d" % angle)

        return data_pb2.ResData(logid=angle)


def main():
    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(
        max_workers=g_worker_num))
    rpc_pb2_grpc.add_RPCServicer_to_server(PredictServer(), server)
    server.add_insecure_port(g_server_addr)
    server.start()

    logging.info("Start PredictServer(%s) Successfully ..." % g_server_addr)

    try:
        while True:
            time.sleep(g_sleep_time)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    main()

# vim: set ts=4 sw=4 sts=4 tw=100: 
