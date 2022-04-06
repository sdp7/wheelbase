#!/usr/bin/env python3


from psutil import POSIX
from rospkg import get_ros_home
import rospy
from geometry_msgs.msg import PoseStamped
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Odometry

class NavClient:
    def __init__(self):
       rospy.init_node('go_back')
       # data for real arena 
       self.goals =  [(0,0,0,0)]
       #self.goals =  [(-0.1845, -0.5100, -0.0857, 0.9963), (1.6050, -0.5800, -0.69536, 0.71866), (1.5550, 1.3600, 0.9703, 0.2420), (-1.065, 1.74, -0.97685, 0.2139), (-2.0150, -0.5000, -6.6721, 1.0000)]
       self.goal_index = 0

       rospy.on_shutdown(self.shutdown)

       self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
       self.client.wait_for_server()
    
    def odom_callback(self,msg):
        print("--------------------------")
        print("pose x = " + str(msg.pose.pose.position.x))
        print("pose y = " + str(msg.pose.pose.position.y))

    def subscriber(self):
        rospy.Subscriber('/odom',Odometry, self.odom_callback)

    def publishMoveBaseGoal(self):
        msg = MoveBaseGoal()
        currGoal = self.goals[self.goal_index]
        msg.target_pose.header.frame_id = "map"
        msg.target_pose.header.stamp = rospy.Time.now()
        msg.target_pose.pose.position.x = currGoal[0]
        msg.target_pose.pose.position.y = currGoal[1]
        msg.target_pose.pose.orientation.z = 0
        msg.target_pose.pose.orientation.w = 1
        print("navgate to point" + str(currGoal[0]) + "," + str(currGoal[1]))
        self.client.send_goal(msg)
        wait = self.client.wait_for_result()
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
            exit()
        else:
            now = rospy.get_rostime()
            self.goal_index = (self.goal_index+1) % len(self.goals)
            return self.client.get_result()
    
    def shutdown(self):
        self.client.cancel_all_goals()
        rospy.loginfo("Stop")
        rospy.sleep(1)
        
if __name__ == '__main__':

    navC = NavClient()
    while True:
        try:
            navC.publishMoveBaseGoal()
            exit()
        except KeyboardInterrupt:
            print("Shutting down")
            exit()
