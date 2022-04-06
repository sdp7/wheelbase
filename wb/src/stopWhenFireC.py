#!/usr/bin/env python3
from itertools import count
from tkinter.tix import Meter

from numpy import angle

from sensor_msgs.msg import JointState
from std_msgs.msg import Bool
import rospy
from geometry_msgs.msg import Twist 
from time import time 
from armMover import *
from geometry_msgs.msg import Twist
import sys

PI = 3.1415926535897

class fireTuner:
    def __init__(self):
        rospy.init_node('twist_to_arm', anonymous=True)
        self.angle = 0
        self.eject = False
        self.moved = False

        self.joint_sub = rospy.Subscriber("joint_states", JointState, self.rotate_callback)

    
    def rotate_callback(self, msg):
        self.angle = msg.position[2]
        print(f"angle read now {self.angle}")
        if (round(self.angle,6) != 0):
            self.rotate(self.angle)

    def move_motor(self): 
        pub = rospy.Publisher('cmd_vel',Twist,queue_size = 10) 
        mc = Twist() 
        mc.linear.x = 0
        mc.angular.z = -self.angle/2
        print(self.angle)
        pub.publish(mc) 

    def rotate(self,angle):
        velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        vel_msg = Twist()

        # Converting from angles to radians
        speed = 60
        angular_speed = speed*2*PI/360
        print(f"print angular speed {angular_speed}")
        relative_angle = -angle
        # relative_angle = angle*2*PI/360

        # Not using linear components because rotating in-place
        vel_msg.linear.x=0
        vel_msg.linear.y=0
        vel_msg.linear.z=0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0


        # Checking if our movement is CW or CCW
        vel_msg.angular.z = -angular_speed

        # Setting the current time to compute angular distance
        t0 = rospy.Time.now().to_sec()
        current_angle = 0

        while(current_angle < relative_angle):
            velocity_publisher.publish(vel_msg)
            t1 = rospy.Time.now().to_sec()
            current_angle = angular_speed*(t1-t0)


        # Robot in the specified angle, so stop
        vel_msg.angular.z = 0
        velocity_publisher.publish(vel_msg)
        move_arm_back()
        # rospy.spin()


def move_arm_back():
    print("mving arm back now")
    am = armMover()
    
    goals = [0.0] * 10
    try:
        for goal in goals:
                am.move_arm(goal) 
                am.rate.sleep() 
    except KeyboardInterrupt:
            print("Shutting down")
            
    statepub.publish(True) 
    sys.exit()

if __name__ == '__main__':
    
    ft = fireTuner()
    st = time()

    statepub = rospy.Publisher('moved_arm', Bool, queue_size =10)
    statepub.publish(False) 

    before_time = rospy.get_time()

    while (not rospy.is_shutdown()):
        try:
            statepub.publish(False) 
            
        except KeyboardInterrupt:
            print("Shutting down")
            break
        



        

