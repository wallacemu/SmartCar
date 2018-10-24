#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: camera.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/10/06 15:54:52
Brief: To take pictures by the camera on the car.
"""

import io
import time
import logging
import traceback
from PIL import Image
from picamera import PiCamera

from timer import Timer


class Camera(object):
    """ Take pictures.
    """
    _resolution = (32, 32)

    def __init__(self, resolution = None):
        if resolution:
            self._resolution = resolution

        self.out_stream = io.BytesIO()
        # camera
        self.camera = PiCamera()
        self.__configure__()
        # warm up the camera
        time.sleep(2)
        # capturer
        self.capturer = self.camera.capture_continuous(
                self.out_stream,
                format='jpeg',
                use_video_port=True)     # 视频端口拍照更快

    def __configure__(self):
        """ To set the configuration of the camera. 
        """
        self.camera.resolution = self._resolution
        self.camera.framerate = 50
        self.camera.hflip = True    # 上下反转，倒置安装
        self.camera.vflip = True    # 左右反转，需要小车视角判别左右

    def __enter__(self):
        return self

    def __exit__(self, exe_type, exe_val, exe_trace):
        self.exit()
        if exe_trace and exe_type != KeyboardInterrupt:
            logging.info("[Camera] %s" % traceback.format_exc(exe_trace))

        return True

    def exit(self):
        del self.capturer    # 先销毁生成器，否则退出会有KeyError
        self.camera.close()
        logging.info("[Camera] close and exit.")

    def capture(self):
        """ return image-stream and Image-object
        """
        # clean out_stream
        self.out_stream.seek(0)
        self.out_stream.truncate()
        # take pic
        t = Timer()
        self.capturer.next()

        return self.out_stream.getvalue(), Image.open(self.out_stream), t.elapse()


# vim: set ts=4 sw=4 sts=4 tw=100: 
