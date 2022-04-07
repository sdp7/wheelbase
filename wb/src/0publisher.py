#!/usr/bin/env python

import queue
import rospy
from std_msgs.msg import Int16
from std_msgs.msg import Float32MultiArray
import RPi.GPIO as GPIO           
from time import sleep 

class ZeroPublisher():
    def __init__(self):
        rospy.init_node("currMode") 

        self.currMode = 0
        self.pumpSwitch = 0
        self.pub = rospy.Publisher("currMode", Int16, queue_size =10)
        self.sub = rospy.Subscriber("manualServer", Float32MultiArray, manual_callback)



    def pubMode(self):
        self.pub.publish(self.currMode)

    def manual_callback(self, msg):
        if msg.data[5] != self.currMode:
            self.currMode = msg.data[5]
            print("change to mode " + str(self.currMode))
        
        if msg.data[4] != self.pumpSwitch:
            if msg.data[4] == 1.0:
                GPIO.output(23, 1)
                print("now is 1")
            else:
                GPIO.output(23, 0)
                print("now is 0")
            print("current pump switch " + str(msg.data[4]))
        


if __name__ == '__main__':


    GPIO.setmode(GPIO.BCM)            
    GPIO.setup(23, GPIO.OUT) 

    zeroPub = ZeroPublisher()

    while not rospy.is_shutdown():
        try:
            zeroPub.pubMode()
        except KeyboardInterrupt:
            print("shutting down")
            exit()
