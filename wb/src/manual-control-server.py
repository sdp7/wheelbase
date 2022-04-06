#!/usr/bin/env python3

'''
Example usage of the TCPServer class from the TCPCOM library
'''

from tcpcom import TCPServer
import rospy
from std_msgs.msg import Float32MultiArray
from time import time, sleep 

# connection configuration settings
tcp_ip = "192.168.105.17"
tcp_port = 6005
tcp_reply = "Manual control message"

wheelbase_x = 0
wheelbase_y = 0
turret_x = 0
turret_y = 0


class manualServer:
    
    def __init__(self):
        rospy.init_node("manual_server", anonymous=True)
        self.wheelbase_x = 0
        self.wheelbase_y = 0
        self.turret_x = 0
        self.turret_y = 0
        self.isShooting = False
        self.control = False
        self.pub = rospy.Publisher("manualServer", Float32MultiArray, queue_size = 10)
        self.rate = rospy.Rate(20)

    def handleMessage(self, msg):
        message = msg.split(";")
        if(message[0] == "Wheelbase"):
            self.wheelbase_x = float(message[1])
            self.wheelbase_y = float(message[2])
        elif(message[0] == "Turret"):
            self.turret_x = float(message[1])
            self.turret_y = float(message[2])
        elif(message[0] == "Shot"):
            if(message[1] == "true"):
                self.isShooting = True
                print("current status is True")
            else:
                self.isShooting = False
                print("current status is False")
        elif (message[0] == "Control"):
            if(message[1] == "true"):
                self.control = True
            else: self.control = False
        self.pub_states()

    def onStateChanged(self, state, msg):
        global isConnected
        try:
            if state == "LISTENING":
                print("Server:-- Listening...")
            elif state == "CONNECTED":
                isConnected = True
                print("Server:-- Connected to" + msg)
            elif state == "MESSAGE":
                print("Server:-- Message received:", msg)
                self.handleMessage(msg)
                server.sendMessage(tcp_reply)
        except KeyboardInterrupt:
            print("Shutting down manual control node")
            exit()
        
    def pub_states(self):
        msg = Float32MultiArray()
        msg.data = [self.wheelbase_x, self.wheelbase_y, self.turret_x, self.turret_y,self.isShooting,self.control]
        self.pub.publish(msg)
        self.rate.sleep()

def main():
    ms = manualServer()
    global server
    server = TCPServer(tcp_port, stateChanged=ms.onStateChanged)
    # while not rospy.is_shutdown():
    #     try:
    #         pass
    #     except KeyboardInterrupt:
    #         print("Shutting down manual control node")
    #         break

if __name__ == '__main__':
    main()