#!/usr/bin/env python3

from doctest import master
import rospy
from std_msgs.msg import Int16
import server

class StatusPoster():

    def __init__(self):
        rospy.init_node("statusPoster")

        self.humanCount = 0
        # 0 for navigation 1 for manual 
        self.currMode = 0

        self.subMode = rospy.Subscriber('currMode', Int16, self.mode_callback)
        self.subHuman = rospy.Subscriber('num_people', Int16, self.humanCount_callback)
        self.rate = rospy.Rate(10)
    
    def mode_callback(self, msg):

        if(msg.data != self.currMode):
            print ("data change to " +  str(msg.data))
            self.currMode = msg.data
    
    def humanCount_callback(self, msg):

        self.humanCount = msg.data
        print("got " + str(self.humanCount) + " human")
    


if __name__ == '__main__':

    statusPoster = StatusPoster()
    server.start_socket()
    while not rospy.is_shutdown():
        try:
            server.send_message(statusPoster.currMode)
            #statusPoster.humanCount
            rospy.spin()
        except KeyboardInterrupt:
            server.close_socket()
            print("shutting down")
            exit()
        master.rate.sleep()

