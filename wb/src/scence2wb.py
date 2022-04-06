#!/usr/bin/env python3

from ast import Pass
from driveToFire import *
from stopWhenFireC import *

class scence2wb():
    def __init__(self):
        rospy.init_node("master_s2_wb")
        self.drive = driveToFire()
        self.stopFire = fireTuner()


if __name__ == '__main__':

    s2wb = scence2wb()

    before_time = rospy.get_time()

    while rospy.get_time() < before_time+2:
        try:
            s2wb.stopFire.move_motor()
        except rospy.ROSInterruptException:
            pass
    
    s2wb.stopFire.angle = 0
    s2wb.stopFire.move_motor()

    while not rospy.is_shutdown():
        try:
            s2wb.drive.move_motor()
            if(s2wb.drive.distantToFire <= 2 and driver.distantToFire >= 1):
                exit()
        except KeyboardInterrupt:
            print("shutting down")
            exit()