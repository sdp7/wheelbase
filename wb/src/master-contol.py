#!/usr/bin/env python3

from navArena import *
from mannualControl import *
from std_msgs.msg import Int16
from time import time, sleep 

class masterControl():
    
    def __init__(self):
        rospy.init_node("masterControl")

        # 0 for navigation and 1 for mannalControl
        self.currMode = 1
        self.sub = rospy.Subscriber('currMode', Int16, self.mode_callback)
        self.nav = NavClient()
        self.mannual = mannualController()
        self.rate = rospy.Rate(20)
    
    def mode_callback(self, msg):
        if(msg.data != self.currMode):
            if(msg.data == 1):
                self.nav.client.cancel_all_goals()
                self.nav.goal_index = (self.nav.goal_index - 1) % len(self.nav.goals)
                print("switch to mannal control")
            elif (msg.data == 0):
                print("switch to navigation")
            else:
                print("exception mode")
                exit()
            
            self.currMode = msg.data

if __name__ == '__main__':

    master = masterControl()

    while not rospy.is_shutdown():
        try:
            if master.currMode == 1:
                master.mannual.move_motor()
            else:
                master.nav.publishMoveBaseGoal()
        except KeyboardInterrupt:
            print("shutting down")
            exit()
        master.rate.sleep()
        

