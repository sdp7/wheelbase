#!/usr/bin/env python3

import posix
from pydoc import cli
from socket import MsgFlag
from sysconfig import get_config_h_filename
from turtle import pos
from cupshelpers import Printer

from psutil import POSIX
from rospkg import get_ros_home
import rospy
from geometry_msgs.msg import PoseStamped
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Odometry

class NavClient:
    def __init__(self):
       rospy.init_node('nav_stack_goals')
       self.goals =  [(0,0,0,0),(1.105, -0.49, -0.5635, 0.826), (1.82215,-3.46746, 0.9999, 0.0097), (-0.1357, -3.27549,0.70201, -0.712166 ), (0,0,0,0)]
       self.goal_index = 0

       self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
       self.client.wait_for_server()
    
    def odom_callback(self,msg):
        print("--------------------------")
        print("pose x = " + str(msg.pose.pose.position.x))
        print("pose y = " + str(msg.pose.pose.position.y))

    def subscriber(self):
        rospy.Subscriber('/odom',Odometry, self.odom_callback)

    def publishMoveBaseGoal(self):
        msg = MoveBaseGoal()
        currGoal = self.goals[self.goal_index]
        msg.target_pose.header.frame_id = "map"
        msg.target_pose.header.stamp = rospy.Time.now()
        msg.target_pose.pose.position.x = currGoal[0]
        msg.target_pose.pose.position.y = currGoal[1]
        msg.target_pose.pose.orientation.z = currGoal[2]
        msg.target_pose.pose.orientation.w = currGoal[3]

        self.client.send_goal(msg)
        wait = self.client.wait_for_result()
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        else:
            now = rospy.get_rostime()
            self.goal_index = (self.goal_index+1) % len(self.goals)
            return self.client.get_result()
        
if __name__ == '__main__':

    navC = NavClient()
    while True:
        try:
            navC.publishMoveBaseGoal()
        except KeyboardInterrupt:
            print("Shutting down")
            exit()



        

