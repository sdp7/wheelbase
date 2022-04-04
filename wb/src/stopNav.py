#!/usr/bin/env python3

from pydoc import cli
from socket import MsgFlag
from turtle import pos

from psutil import POSIX
import rospy
from geometry_msgs.msg import PoseStamped
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Odometry


if __name__ == '__main__':
    rospy.init_node('stopper')
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    client.cancel_all_goals()
    exit()