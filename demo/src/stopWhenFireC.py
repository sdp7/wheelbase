#!/usr/bin/env python3
from itertools import count
from tkinter.tix import Meter

from numpy import angle

from sensor_msgs.msg import JointState
import rospy
from geometry_msgs.msg import Twist 
from time import time 

class fireTuner:
    def __init__(self):
        rospy.init_node('arm_mover', anonymous=True)
        self.angle = 0


        self.joint_sub = rospy.Subscriber("joint_states", JointState, self.rotate_callback)

    
    def rotate_callback(self, msg):
        print("---------------------------------")
        print("arm radius is" + str(msg.position[2]))
        self.angle = msg.position[2]

    def move_motor(self): 
        pub = rospy.Publisher('cmd_vel',Twist,queue_size = 10) 
        mc = Twist() 
        mc.linear.x = 0
        mc.angular.z = self.angle 
        pub.publish(mc) 

if __name__ == '__main__':
    
    ft = fireTuner()
    st = time()
    while (not rospy.is_shutdown()):
        try:
            if  (round(ft.angle,3) != 0):
                before_time = rospy.get_time()
                
                while rospy.get_time()<before_time+2: 
                    try: 
                        ft.move_motor() 
                    except rospy.ROSInterruptException: 
                        pass 
                else: 
                    ft.angle = 0
                    ft.move_motor()

                print(rospy.get_time() - before_time)
                exit()

            
            
        except KeyboardInterrupt:
            print("Shutting down")
            break
            exit()