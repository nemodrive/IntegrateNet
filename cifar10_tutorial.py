#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division
import torch
from PIL import Image
import torchvision
import torchvision.transforms as transforms
import os
import pandas as pd
# from skimage import io, transform
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
import torch.nn as nn
import torch.nn.functional as F
i=0
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(317, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        self.fc4 = nn.Linear(10, 1)

    def forward(self, x):
        global i
	x = self.conv1(x)
        # x = self.pool(F.relu(self.conv1(x)))
        # x = self.pool(F.relu(self.conv2(x)))
        # (1, 16, 317, 177)
        # x = x.view(-1, 317) #(1, 16, 267, 317)
        # x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))
        # x = F.relu(self.fc3(x))
        # x = self.fc4(x)
        # x = x.detach()
        # x = x.numpy()
        # x = np.mean(x)
        return x

OUTPUT_TOPIC = "/local_steer_net"

# Subscriber part
#net = Net()
#net = net.cuda()
i = 0
def callback(img, pub):
    global i
    im = img.data
    timestamp = str(img.header.stamp.secs) + " " + str(img.header.stamp.nsecs) 
    d = []
   # d = np.frombuffer(im, dtype=np.uint8)
   # img = d.reshape((720, 1280, 2))
   # img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_YUY2)
   # img = img.transpose(2, 1, 0)

   # py_img = torch.from_numpy(img)
   # py_img = py_img.unsqueeze(0)
   # py_img = py_img.type(torch.FloatTensor)
   # py_img = py_img.cuda()
   # output = net.forward(py_img)
   # output = output.min().cpu()
    pub.publish(str(timestamp))

def main():
    rospy.init_node('img_republisher')
    pub = rospy.Publisher(OUTPUT_TOPIC, String, queue_size= 10)
    rospy.Subscriber("/apollo/sensor/camera/traffic/image_long", Image, callback, pub, queue_size=10)
    rospy.spin()

if __name__ == '__main__':
    main()

#  - bazel-apollo/modules/drivers/camera
# - bazel-apollo/modules/drivers/usb_cam
