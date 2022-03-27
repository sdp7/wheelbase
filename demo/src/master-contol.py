#!/usr/bin/env python3

from navArena import *
from mannualControll import *
from std_msgs.msg import Int16

class masterControl():
    
    def __init__(self):
        rospy.init_node("master-control", anonymous = True)

        # 0 for navigation and 1 for mannalControl
        self.currMode = 0
        self.sub = rospy.Subscriber('currMode', Int16, self.mode_callback)
        self.nav = NavClient()
        self.mannual = mannualController()
    
    def mode_callback(self, msg):
        if(msg.data != self.currMode):
            if(msg.data == 1):
                self.nav.client.cancel_all_goals()
                print("switch to mannal control")
            elif (msg.data == 0):
                print("switch to navigation")
            else:
                print("exception mode")
                exit()
            
            self.currMode = msg.data

if __name__ == '__main__':

    master = masterControl()

    if master.currMode == 1:
        master.mannual.move_motor()
    else:
        master.nav.publishMoveBaseGoal()
        

