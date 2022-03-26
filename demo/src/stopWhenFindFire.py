#!/usr/bin/env python3

from itertools import count
from tkinter.tix import Meter

import rospkg
from sensor_msgs.msg import JointState
import rospy
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import LaserScan 
from time import time 


def rotate_callback(msg):
    print("---------------------------------")
    print("arm radius is" + str(msg.position[2]))
    
    angle_rad = (msg.position[2])

    return angle_rad

def move_motor(fwd,ang,duration): 
    pub = rospy.Publisher('cmd_vel',Twist,queue_size = 10) 
    mc = Twist() 
    mc.linear.x = fwd
    mc.angular.z = ang 
    start_time = time()

    while time() < start_time + duration:
        pub.publish(mc)
    else:
        mc.linear.x = 0
        mc.angular.z = 0
        pub.publish(mc)

if __name__ == '__main__':
    rospy.init_node('arm_mover')
    angle = rospy.Subscriber("joint_states", JointState, rotate_callback)
    #rospy.spin()
    print("hello")
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        move_motor(0, angle[0]/2, 2)
        rate.sleep()
        exit()

    
