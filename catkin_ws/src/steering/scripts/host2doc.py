#!/usr/bin/env python
import rospy
import time
# ROS Image message
from std_msgs.msg import String
import numpy as np
# INPUT_TOPIC = "/apollo/sensor/camera/traffic/image_long"
INPUT_TOPIC = "/local_steer_net"
OUTPUT_TOPIC = "/docker_steer_net"
timestamps = []
counter = 0
def callback(img, pub):
    global timestamps
    global counter
    time = img.data.split(" ")
    nsecs = time[1]
    secs = time[0]
    print(secs)
    print(rospy.Time.now().secs)
    if(float(secs) == rospy.Time.now().secs and rospy.Time.now().nsecs >= float(nsecs)):
	print("GOT IN")
	timestamps.append(rospy.get_rostime().nsecs - float(nsecs))
        counter = counter + 1

    if(counter < 30):
  	print("right branch")
  #  	print(rospy.Time.now().secs)


    v = np.array(timestamps)
    if(counter == 30):
    	print(v.mean(), v.std())
    pub.publish(img)

def main():
    rospy.init_node('host2doc')
    pub = rospy.Publisher(OUTPUT_TOPIC, String, queue_size= 10)
    rospy.Subscriber(INPUT_TOPIC, String, callback, pub, queue_size=10)
    rospy.spin()

if __name__ == '__main__':
    main()
