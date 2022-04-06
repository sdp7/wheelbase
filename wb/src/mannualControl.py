#!/usr/bin/env python3


from numpy import angle

from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import JointState
import rospy
from geometry_msgs.msg import Twist 
from time import time 

class mannualController():
    def __init__(self):
        rospy.init_node("mannal_control", anonymous=True)
        self.angSpeed = 0
        self.linSpeed = 0

        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.sub = rospy.Subscriber('manualServer', Float32MultiArray,self.control_callback)

    def control_callback(self, msg):
        print("curr linear speed is" + str(msg.data[1]))
        print("curr angle speed is" + str(msg.data[0]))

        print("hello")
        self.linSpeed = 0.23 * msg.data[1]
        self.angSpeed = -1.82 * msg.data[0]

    def move_motor(self): 
        mc = Twist() 
        mc.linear.x = self.linSpeed
        mc.angular.z = self.angSpeed 
        self.pub.publish(mc) 
        print(self.linSpeed)
        print(self.angSpeed)


if __name__ == '__main__':

    controller = mannualController()

    while not rospy.is_shutdown():
        try:
            controller.move_motor()
        except KeyboardInterrupt:
            print("shutting down")
            exit()
    