#!/usr/bin/env python3

from pydoc import cli
from socket import MsgFlag
from sysconfig import get_config_h_filename
from turtle import pos

from psutil import POSIX
import rospy
from geometry_msgs.msg import PoseStamped
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Odometry

def odom_callback(msg):
    print("--------------------------")
    print("pose x = " + str(msg.pose.pose.position.x))
    print("pose y = " + str(msg.pose.pose.position.y))

def subscriber():
    rospy.Subscriber('/odom',Odometry, odom_callback)


def talker():
    rospy.init_node('talker', anonymous=True)
    
    pub = rospy.Publisher("/move_base", MoveBaseGoal, queue_size= 10)
    msg = MoveBaseGoal()

    msg.target_pose.header.stamp = rospy.Time.now()
    msg.target_pose.header.frame_id = 'map'
    msg.target_pose.pose.position.x = 0.0
    msg.target_pose.pose.position.y = 0.0
    msg.target_pose.pose.orientation.w = 1.0
    rate = rospy.Rate(10)
    rospy.loginfo(msg)
    pub.publish(msg)

def publishMoveBaseGoalWaitForReply(posX, posY, oriZ, oriW):
    rospy.init_node('talker', anonymous=True)
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = posX
    goal.target_pose.pose.position.y = posY
    goal.target_pose.pose.orientation.z = oriZ
    goal.target_pose.pose.orientation.w = oriW

    # to send orientation with a yaw we need quaternion transform
    goal.target_pose.pose.orientation.w = 1.0
    now = rospy.get_rostime()

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    # publish the goal to the topic
    client.send_goal(goal)
    now = rospy.get_rostime()
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        now = rospy.get_rostime()
        return client.get_result()

if __name__ == '__main__':
    
    # goals = [(0, -0, 0, 0),(1.29,-0.41, -0.380, -0.9254),(1.157, 1.20, -0.12,1),(3.32, 1.42, -0.52, 0.85), (3.69, -0.73, -0.9889, 0.15), (0,0,0,0)]

    goals = [(0,0,0,0),(1.105, -0.49, -0.5635, 0.826), (1.82215,-3.46746, 0.9999, 0.0097), (-0.1357, -3.27549,0.70201, -0.712166 ), (0,0,0,0)]
    
    goal_index = 0

    try:
        # talker()
        # print("hello world")
        # # publishMoveBaseGoalWaitForReply()
        # subscriber()
        for goal in goals:
            print(goal[0])
            print(goal[1])
            publishMoveBaseGoalWaitForReply(goal[0],goal[1],goal[2], goal[3])

        while goal_index < len(goals):
            print(goal[0])
            print(goal[1])
            publishMoveBaseGoalWaitForReply(goal[0],goal[1],goal[2], goal[3])
            goal_index = goal_index + 1

    except rospy.ROSInterruptException:
        pass

