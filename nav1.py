#!/usr/bin/env python
import rospy
import actionlib
import tf2_ros
import numpy as np
import sys
import random
import math
from geometry_msgs.msg import Transform, TransformStamped, Vector3, Quaternion
from sensor_msgs.msg import LaserScan
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal 
from time import time 


class Scan():
    def __init__(self):
        self.__move_base_client = actionlib.SimpleActionClient('move_base',
                                                               MoveBaseAction)
        self.__move_base_client.wait_for_server()
        self.__tf_broadcaster = tf2_ros.TransformBroadcaster()
        self.__tf_buffer = tf2_ros.Buffer()
        self.__tf_listener = tf2_ros.TransformListener(self.__tf_buffer)

    

if __name__ == '__main__': 
    rospy.init_node('nav1',anonymous=True)

    while time()<start_time+5: 
        try: 
            read_laser_scan_data() 
            move_motor(forward_speed,turn_speed) 
        except rospy.ROSInterruptException: 
            pass  
  