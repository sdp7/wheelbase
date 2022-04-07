#!/usr/bin/env python3
import rospy
import math
import numpy as np
from sensor_msgs.msg import JointState 
from std_msgs.msg import Float32MultiArray, Float64MultiArray
from time import time, sleep 
 
# processes the data from the ROSTopic named "joint_states"
class manual_aim:
    def __init__(self):
        rospy.init_node('move_arm',anonymous=True)
        self.manual_server_rate = 10
        self.rate = rospy.Rate(self.manual_server_rate)
        self.jointpub = rospy.Publisher('joint_trajectory_point',Float64MultiArray, queue_size =10)    
        self.joint_pos = Float64MultiArray()
        self.current_pos = []
        rospy.Subscriber("joint_states",JointState, self.joint_callback)  
        rospy.Subscriber("manualServer", Float32MultiArray, self.arm_callback)

    def joint_callback(self,data): 
        theta1 = data.position[2]
        theta2 = data.position[5]

        self.current_pos = [theta1, theta2]

    def arm_callback(self,data):
        base_velocity = data.data[2]
        turret_velocity = data.data[3]
        dt = 1 / self.manual_server_rate

        displacement_base = base_velocity * dt
        displacement_turret = turret_velocity * dt
        
        self.current_pos[0] = self.current_pos[0] - displacement_base
        self.current_pos[1] = self.current_pos[1] - displacement_turret

        self.move_arm(self.current_pos[0], self.current_pos[1])
    
    # Makes sure the joints do not go outside the joint limits/break the servos
    def clean_joint_states(self,data): 
        lower_limits = [0, -3.14, -1.57, -1.57, -1, -1] 
        upper_limits = [0,  3.14,  1.57,  1.57,  1.57, 1] 
        clean_lower = np.maximum(lower_limits,data) 
        clean_upper = np.minimum(clean_lower,upper_limits) 
        return list(clean_upper) 
    
    # publishes a set of joint commands to the 'joint_trajectory_point' topic
    def move_arm(self,base_angle, turret_angle):
        #Joint Position vector should contain 6 elements:
        #[0, shoulder1, shoulder2, elbow, wrist, gripper]

        self.joint_pos.data = self.clean_joint_states([0, base_angle, 1.57, -1.47, turret_angle, 0])
        self.jointpub.publish(self.joint_pos)

 
#loops over the commands at 20Hz until shut down
if __name__ == '__main__': 
    aimer = manual_aim()

    while not rospy.is_shutdown():
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("Shutting down")
