#!/usr/bin/env python3
import rospy 
from numpy import maximum,minimum 
from sensor_msgs.msg import JointState 
from std_msgs.msg import Float64MultiArray, Bool
from time import time, sleep 

class armMover():
    def __init__(self):
        rospy.init_node('move_arm',anonymous=True) 
        self.jointpub = rospy.Publisher('joint_trajectory_point',Float64MultiArray, queue_size =10)    
        self.joint_pos = Float64MultiArray() 
        self.rate = rospy.Rate(1)
        self.joint_sub = rospy.Subscriber("joint_states",JointState, self.joint_callback)


    # processes the data from the ROSTopic named "joint_states"
    def joint_callback(self,data): 
        print("Msg: {}".format(data.header.seq)) 
        print("Wheel Positions:\n\tLeft: {0:.2f}rad\n\tRight: {0:.2f}rad\n\n".format(data.position[0],data.position[1])) 
        print("Joint Positions:\n\tShoulder1: {0:.2f}rad\n\tShoulder2: {0:.2f}rad\n\tElbow: {0:.2f}rad\n\tWrist: {0:.2f}rad\n\n".format(data.position[2],data.position[3],data.position[4],data.position[5])) 
        print("Gripper Position:\n\tGripper: {0:.2f}rad\n".format(data.position[6])) 
        print("----------") 
    
    # listens to the "joint_states" topic and sends them to "joint_callback" for processing
    def read_joint_states(self): 
        rospy.Subscriber("joint_states",JointState, self.joint_callback) 
    
    # Makes sure the joints do not go outside the joint limits/break the servos
    def clean_joint_states(self,data): 
        lower_limits = [0, -1.57, -1.57, -1.57, -1.57,   -1] 
        upper_limits = [0,  1.57,  1.57,  1.57,  1.57, 1.57] 
        clean_lower = maximum(lower_limits,data) 
        clean_upper = minimum(clean_lower,upper_limits) 
        return list(clean_upper) 
    
    # publishes a set of joint commands to the 'joint_trajectory_point' topic
    def move_arm(self,angle): 
        #Joint Position vector should contain 6 elements:
        #[0, shoulder1, shoulder2, elbow, wrist, gripper]
        self.joint_pos.data = self.clean_joint_states([0, angle,  1.57, -1.47, 0, 0]) 
        self.jointpub.publish(self.joint_pos) 
        self.read_joint_states() 
 
#loops over the commands at 10Hz until shut down
if __name__ == '__main__': 
    num = 0
    am = armMover()

    statepub = rospy.Publisher('reset_arm', Bool, queue_size =10)
    statepub.publish(False) 
    goals = [0.0]*10
    while not rospy.is_shutdown(): 
        for goal in goals:
            am.move_arm(goal) 
            am.rate.sleep() 
        exit()
