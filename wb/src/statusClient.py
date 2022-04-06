#!/usr/bin/env python3

from doctest import master
import rospy
from std_msgs.msg import Int16
import server
from std_msgs.msg import Float32MultiArray

class StatusPoster():

    def __init__(self):
        rospy.init_node("statusPoster")

        self.humanCount = 0
        # 0 for navigation 1 for manual 
        self.currMode = 0.0

        self.subMode = rospy.Subscriber('manualServer', Float32MultiArray, self.mode_callback)
        # self.subHuman = rospy.Subscriber('num_people', Int16, self.humanCount_callback)
        self.rate = rospy.Rate(1)
    
    def mode_callback(self, msg):
        if(msg.data[5] != self.currMode):
            print ("data change to " +  str(msg.data))
            self.currMode = msg.data[5]
            self.rate.sleep()
    # def humanCount_callback(self, msg):
    #     self.humanCount = msg.data
    #     print("got " + str(self.humanCount) + " human")
    

if __name__ == '__main__':

    statusPoster = StatusPoster()
    server.start_socket()
    lastStatus = 0.0
    while not rospy.is_shutdown():
        try:
            server.send_message(str(statusPoster.currMode))
            print(str(statusPoster.currMode))
            statusPoster.rate.sleep()
            #statusPoster.humanCount
            # rospy.spin()
        except:
            server.close_socket()
            print("shutting down")
            exit()
            break

