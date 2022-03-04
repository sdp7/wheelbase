#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Transform, TransformStamped, Vector3, Quaternion
from sensor_msgs.msg import LaserScan
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal 
from time import time 

class Scan():
    def initialise():
        pub = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size=10)
        initpose = PoseWithCovarianceStamped()
        initpose.header.stamp = rospy.get_rostime()
        initpose.header.frame_id = "map"
        initpose.pose.pose.position.x = x
        initpose.pose.pose.position.y = y
        quaternion = get_quaternion(theta)
        initpose.pose.pose.orientation.w = quaternion[0]
        initpose.pose.pose.orientation.x = quaternion[1]
        initpose.pose.pose.orientation.y = quaternion[2]
        initpose.pose.pose.orientation.z = quaternion[3]
        pub.publish(init_pose)

    def callback

if __name__ == '__main__': 
    rospy.init_node('nav1',anonymous=True)

    while time()<start_time+5: 
        try: 
            read_laser_scan_data() 
            move_motor(forward_speed,turn_speed) 
        except rospy.ROSInterruptException: 
            pass  
  