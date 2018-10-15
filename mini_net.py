#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division
import torch
from PIL import Image
import torchvision
import torchvision.transforms as transforms
from cv_bridge import CvBridge
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from rgb2yuv_yuv2rgb import *
import rospy
# ROS Image message
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv2 import *
import time

import matplotlib.pyplot as plt
import numpy as np

import torch.nn as nn
import torch.nn.functional as F
i=0
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(267, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        self.fc4 = nn.Linear(10, 1)

    def forward(self, x):
        global i
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 267) #(1, 16, 267, 317)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        x = x.detach()
        x = x.numpy()
        x = np.mean(x)
        return x

OUTPUT_TOPIC = "/local_steer_net"

net = Net()
def callback(img, pub):
    start_time = time.time()
    im = img.data
    d = []
    d = np.frombuffer(im, dtype=np.uint8)
    d = d.reshape(3, int(len(d)/img.step), int(img.step/3))
    # print("--- %s seconds ---" % (time.time() - start_time))
    py_img = torch.from_numpy(d)
    py_img = py_img.unsqueeze(0)
    py_img = py_img.type(torch.FloatTensor)
    output = net.forward(py_img)
    pub.publish(str(output))

def main():
    rospy.init_node('img_republisher')
    pub = rospy.Publisher(OUTPUT_TOPIC, String, queue_size= 10)
    rospy.Subscriber("/steer_net", Image, callback, pub, queue_size=10)
    rospy.spin()

if __name__ == '__main__':
    main()