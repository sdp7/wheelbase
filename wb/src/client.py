#!/usr/bin/env python3
import rospy
import socket
from std_msgs.msg import Bool


class startClient():
    
    def __init__(self):
        rospy.init_node("mainSwitch")
        self.currStatus = 0
        self.s = None
        self.pub = rospy.Publisher("mainSwitch", Bool, queue_size = 10)

   
    def start_socket(self):
        host = '192.168.105.223'
        #host = '129.215.3.209'
        port = 36205

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

    def receive_message(self):
        msg = self.s.recv(1024).decode()
        return msg

        
    def close_socket(self):
        # disconnect the client
        self.s.close()
        print("Socket closed.")

    def publish(self,state):
        if state == "0":
            self.pub.publish(False)
        elif state == "1":
            self.pub.publish(True)
            
        

if __name__ == "__main__":
    c = startClient()
    c.start_socket()
    state = "0"
    try:
        while True:
            message = c.receive_message()
            if message == state:
               c.publish(state)
               print("Received: " + message)
            elif message != state:
               state = message
               c.publish(state)
               print("Received: " + message)
            elif message == "close":
               c.close_socket()
               break
    except:    
        c.close_socket()
