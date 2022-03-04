#!/usr/bin/env python3

from socket import MsgFlag
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

def publishMoveBaseGoalWaitForReply(posX, posY):
    rospy.init_node('talker', anonymous=True)
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = posX
    goal.target_pose.pose.position.y = posY

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
    
    goals = [(0, -0.5), (0, 0.5), (-0.45, -1.2)]

    try:
        # talker()
        # print("hello world")
        # # publishMoveBaseGoalWaitForReply()
        # subscriber()
        for goal in goals:
            print(goal[0])
            print(goal[1])
            publishMoveBaseGoalWaitForReply(goal[0],goal[1])

        
    except rospy.ROSInterruptException:
        pass

