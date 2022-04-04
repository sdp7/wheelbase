#!/usr/bin/env python3

import queue
import rospy
from std_msgs.msg import Bool

class SwitchAmplifier():
    def __init__(self) :
        rospy.init_node("switchAmplifier")
        self.currMode = False
        self.pub = rospy.Publisher("switchAmplifier", Bool, queue_size=10)
        self.sub = rospy.Subscriber("mainSwitch", Bool, self.amp_callback)

    def amp_callback(self, msg):
        print("current mode is " + str(msg.data))

        self.currMode = msg.data

    def amp_pub(self):
        mode = Bool()
        mode.data = self.currMode

        self.pub.publish(mode)

if __name__ == '__main__':

    switchPub = SwitchAmplifier()

    while not rospy.is_shutdown():
        try:
            switchPub.amp_pub()
        except KeyboardInterrupt:
            print("shutting down")
            exit()