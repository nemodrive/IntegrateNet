#!/usr/bin/env python
import rospy
# ROS Image message
from std_msgs.msg import String

# INPUT_TOPIC = "/apollo/sensor/camera/traffic/image_long"
INPUT_TOPIC = "/local_steer_net"
OUTPUT_TOPIC = "/docker_steer_net"

def callback(img, pub):
    print("received")
    pub.publish(img)

def main():
    rospy.init_node('img_rep')
    pub = rospy.Publisher(OUTPUT_TOPIC, String, queue_size= 10)
    rospy.Subscriber(INPUT_TOPIC, String, callback, pub, queue_size=10)
    rospy.spin()

if __name__ == '__main__':
    main()