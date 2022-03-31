#!/usr/bin/env python3

import queue
import rospy
from rospy import Publisher
from std_msgs.msg import Int16

class ZeroPublisher():
    def __init__(self):
        rospy.init_node("currMode")
        self.currMode = 0
        self.pub = rospy.Publisher("currMode", Int16, queue_size =10)

    def pubMode(self):
        self.pub.publish(self.currMode)

if __name__ == '__main__':

    zeroPub = ZeroPublisher()

    while not rospy.is_shutdown():
        try:
            zeroPub.pubMode()
        except KeyboardInterrupt:
            print("shutting down")
            exit()
