import paddle.fluid as fluid

# BN层+Activation function(ReLU)+Conv层 模块
def bn_conv_layer(ipt, ch_out, filter_size, stride, padding, bias_attr=False):
    """
    """
    bn = fluid.layers.batch_norm(input=ipt, act='relu')

    return fluid.layers.conv2d(
            input=bn,
            num_filters=ch_out,
            filter_size=filter_size,
            stride=stride,
            padding=padding,
            act='relu',
            bias_attr=bias_attr)


def shortcut(ipt, ch_in, ch_out, stride):
    if ch_in != ch_out:
        return bn_conv_layer(ipt, ch_out, 1, stride, 0)
    else:
        return ipt


def basicblock(ipt, ch_in, ch_out, stride):
    bn1 = bn_conv_layer(ipt, ch_out, 3, stride, 1)
    bn2 = bn_conv_layer(bn1, ch_out, 3, 1, 1)
    short = shortcut(ipt, ch_in, ch_out, stride)

    return fluid.layers.elementwise_add(x=bn2, y=short, act='relu')


def layer_warp(ipt, ch_in, ch_out, count, stride):
    ## 第一层Block的第一层conv控制步长来降维
    out = basicblock(ipt, ch_in, ch_out, stride)
    ## 后面stride=1，padding=1 大小不变
    for i in range(1, count):
        out = basicblock(out, ch_out, ch_out, 1)
    return out


def resnet_simple(ipt, label_cnt):
    conv1 = fluid.layers.conv2d(
                input=ipt,
                num_filters=4,
                filter_size=3,
                stride=1,
                padding=1,   # 图像大小不变
                act='relu',  # linear
                bias_attr=False)

    pool1 = fluid.layers.pool2d(
            input=conv1,
            pool_size=4,
            pool_type='avg',
            pool_stride=2)

    # block: ch_in=num_filters, ch_out / ch_in = stride
    res1 = layer_warp(ipt=pool1, ch_in=4, ch_out=8, count=1, stride=1)

    pool2 = fluid.layers.pool2d(
            input=res1,
            pool_size=4,
            pool_type='avg',
            pool_stride=2)

    res2 = layer_warp(ipt=pool2, ch_in=8, ch_out=16, count=1, stride=1)
    ## pool_size = 8
    pool3 = fluid.layers.pool2d(
            input=res2,
            pool_size=4,     # 2/4/8 变化不大，越大训练收敛越平稳 波动小
            pool_type='avg',
            pool_stride=1)

    predict = fluid.layers.fc(input=pool3, size=label_cnt, act='softmax')
    return predict


def inference(data_shape, label_cnt):
    """
    data_shape: (C, H, W)
    label_cnt: labels
    """
    def program():
        img = fluid.layers.data(
                name='pixel',
                shape=data_shape,
                dtype='float32')
        return resnet_simple(img, label_cnt)

    return program


# vim: set ts=4 sw=4 sts=4 tw=100:
