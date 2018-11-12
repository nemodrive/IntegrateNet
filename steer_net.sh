#!/bin/bash
cd /apollo
source catkin_ws/devel/setup.bash
roslaunch steering start_steer_transf.launch
