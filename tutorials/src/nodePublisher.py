#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def talker():
    rospy.init_node('talker', anonymous=True)
    
    pub = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size= 10)
    msg = PoseStamped()

    msg.header.seq = 1
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = 'map'
    msg.pose.position.x = -0.0
    msg.pose.position.y = 0.0
    msg.pose.orientation.w = 1.0
    rate = rospy.Rate(10)
    rospy.loginfo(msg)
    pub.publish(msg)

def publishMoveBaseGoalWaitForReply():
    rospy.init_node('talker', anonymous=True)
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 0.5
    goal.target_pose.pose.position.y = -1.3

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
    

    try:
        publishMoveBaseGoalWaitForReply()
    except rospy.ROSInterruptException:
        pass

