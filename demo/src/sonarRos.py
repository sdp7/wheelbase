#!/usr/bin/env python

from dis import dis
import queue
import RPi.GPIO as gpio
import time
import sys
import signal
import rospy
from std_msgs.msg import Float32

class Sonar():
    def __init__(self):
        rospy.init_node("Sonar")
        self.distance = 0
        self.pub = rospy.Publisher("Sonar", Float32, queue_size = 10)

    def pubDis(self):
        self.pub.publish(self.distance)
        

def signal_handler(signal, frame): # ctrl + c -> exit program
        print('You pressed Ctrl+C!')
        sys.exit(0)

if __name__ == '__main__':

    sonar = Sonar()

    signal.signal(signal.SIGINT, signal_handler)

    gpio.setmode(gpio.BCM)
    trig = 18 # th
    echo = 24 # th

    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)

    time.sleep(0.5)
    print ('----------------------------------------sonar start---------------------------')
    try :
        print('trying while loop') 
        while True :
            gpio.output(trig, False)
            time.sleep(1)
            gpio.output(trig, True)
            time.sleep(1)
            gpio.output(trig, False)
            while gpio.input(echo) == 0 :
                pulse_start = time.time()
            while gpio.input(echo) == 1 :
                pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17000
            if pulse_duration >=0.01746:
                print('time out')
                continue
            elif distance > 400 or distance==0:
                print('out of range')
                continue
            distance = round(distance, 3)
            sonar.distance = distance
            print ('Distance : %f cm'%distance)
            sonar.pubDis()
            
    except (KeyboardInterrupt, SystemExit):
        print('keyboard interrupt')
        gpio.cleanup()
        sys.exit(0)
    except:
        print('pins are wrong')
        gpio.cleanup()
