                           

import RPi.GPIO as GPIO           
from time import sleep           
GPIO.setmode(GPIO.BCM)            
GPIO.setup(23, GPIO.OUT)            
  
try:  
    while True:  
        GPIO.output(23, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
        sleep(5)                 # wait half a second  
        GPIO.output(23, 0)         # set GPIO24 to 0/GPIO.LOW/False  
        sleep(5)                 # wait half a second  

except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  