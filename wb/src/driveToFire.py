#!/usr/bin/env python3


import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist 

class driveToFire():
    def __init__(self):
        rospy.init_node("driveToFire")
        self.distantToFire = 2.0

        self.mc = Twist()
        self.mc.linear.x = 0.13
        self.mc.angular.z = 0

        rospy.on_shuwdown(self.shutdown)

        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10)
        self.sub = rospy.Subscriber("FireDis", Float32, self.distance_callback)
    
    def distance_callback(self, msg):
        print("current distance to fire is " + str(msg.data))

        self.distantToFire = msg.date

    def shutdown(self):
        closeMC = Twist()
        closeMC.linear.x = 0
        closeMC.angular.y = 0
        self.pub.publish(closeMC)
        rospy.loginfo("Stop")
        rospy.sleep(1)

    def move_motor(self):
        while not (self.distantToFire <=2 and self.distantToFire >= 1):
            self.pub.publish(self.mc)

if __name__ == '__main__':

    driver = driveToFire()

    while not rospy.is_shutdown():
        try:
            driver.move_motor()
            if(driver.distantToFire <= 2 and driver.distantToFire >= 1):
                exit()
        except KeyboardInterrupt:
            print("shutting down")
            exit()
    




