#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Wallace MU. All Rights Reserved.
 
"""
File: predictor.py
Author: wallacemu(wallacemu@163.com)
Date: 2018/10/08 16:55:11
Brief: predictor
"""

import sys
import numpy as np
import paddle
import paddle.fluid as fluid
from PIL import Image

import resnet


class Predictor(object):
    """
    """
    _model_dir = "./model/"
    _img_size = (32, 32)     # (width, height)
    _label_list = [0, 2, 5, 8, 10]   # The actual labels
    _label_cnt = len(_label_list)

    def __init__(self, model_dir=None, img_size=None):
        if model_dir:
            self._model_dir = model_dir

        if img_size:
            _img_size = img_size
        # C,H,W 
        data_shape = (3, self._img_size[1], self._img_size[0])
        self.inferencer = fluid.Inferencer(
                infer_func=resnet.inference(data_shape, self._label_cnt),
                param_path=self._model_dir,
                place=fluid.CPUPlace())


    def format_input(self, img):
        img = img.resize(self._img_size, Image.ANTIALIAS)
        img = np.array(img).astype(np.float32)
        img = img / 255.0
        img = img.transpose((2, 0, 1))  # To CHW order
        # Add one dimension to mimic the list format.
        img = np.expand_dims(img, axis=0)

        return img


    def predict(self, img):
        img = self.format_input(img)
        ret = self.inferencer.infer({"pixel": img})

        return self._label_list[np.argmax(ret[0])]


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s model image1 image2..." % sys.argv[0])
        exit(0)
    
    predictor = Predictor(model_dir=sys.argv[1])
    for i in range(2, len(sys.argv)):

        img = Image.open(sys.argv[i])
        print sys.argv[i], predictor.predict(img)


# vim: set ts=4 sw=4 sts=4 tw=100:
