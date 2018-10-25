#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: client.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/09/30 21:51:38
Brief: RPC client 
"""

import time
import logging

import grpc
from proto import data_pb2
from proto import rpc_pb2_grpc


class Client():
    _server_addr = "192.168.3.3:8002"
    _timeout_s = 1

    def __init__(self, server_addr = None):
        if server_addr:
            self._server_addr = server_addr
        
        self.channel = grpc.insecure_channel(self._server_addr)
        self.stub = rpc_pb2_grpc.RPCStub(channel=self.channel)

    def send(self, img_str, w=0, h=0):
        data = data_pb2.ReqData()
        data.width = w
        data.height = h
        data.image = bytes(img_str)

        res_data = None
        try:
            res_data = self.stub.run(data, Client._timeout_s)
            #logging.info("[RPCClient][SUCC][id=%d]" % res_data.logid)
        except Exception as e:
            logging.info("[RPCClient][FAIL]" + e.message)
        
        return res_data


def test():
    client = Client()

    avg_time = 0
    loop_cnt = 1000

    for i in range(loop_cnt):
        begin = time.time()
        client.send("Hello")
        end = time.time()
        avg_time += end - begin;

    print("request_time=", avg_time / loop_cnt)
    return 0


if __name__ == '__main__':
    test()

# vim: set ts=4 sw=4 sts=4 tw=100: 
