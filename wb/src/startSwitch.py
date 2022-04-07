#!/usr/bin/env python3

from platform import node

from std_msgs.msg import Bool
import roslaunch
import rospy



class startSwitch():
    def __init__(self):
        rospy.init_node("startSwitch")
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        self.launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/jingyuan/fred_master/src/demo/launch/scanner.launch"])
        self.currSwitchStatus = False
        self.sub = rospy.Subscriber("switchAmplifier", Bool, self.switch_callback)

    def switch_callback(self, msg):
        if(self.currSwitchStatus != msg.data):
            self.currSwitchStatus = msg.data


if __name__ == '__main__':

    switch = startSwitch()
    currSwitch = switch.currSwitchStatus
    while not rospy.is_shutdown():
        try:
            if switch.currSwitchStatus != currSwitch:
                switch.launch.start()
                rospy.loginfo("started")
                currSwitch = switch.currSwitchStatus
        except KeyboardInterrupt:
            print("shutting down")
            switch.launch.shutdown()
            exit()
        