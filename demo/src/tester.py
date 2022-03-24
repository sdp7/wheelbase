#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64MultiArray
import cv2
from cv2 import blur
import numpy as np
import math


def to3D(x,y, area):

    focal_length = 0.0031

    object_size = 0.025
    
    sensor_size_horizontal = 0.00358   # 3.58 x 2.02 mm

    radius = math.sqrt(area/math.pi)

    pixel_to_meter = object_size/radius

    image_size = (sensor_size_horizontal * radius) / 1280

    distance = (object_size * focal_length) / image_size

    z_meter = y * pixel_to_meter

    y_meter = x * pixel_to_meter

    x_meter = distance

    return (x_meter, y_meter, z_meter)

capture = cv2.VideoCapture(0)

rospy.init_node('ball_position')
pub = rospy.Publisher("ball_position", Float64MultiArray, queue_size=10)

while True:

    ret, frame = capture.read()
    blur_frame = cv2.GaussianBlur(frame, (5,5), 0)
    hsv_frame = cv2.cvtColor(blur_frame, cv2.COLOR_BGR2HSV)
    
   # green_lower = np.array([25, 52, 72])
   #green_higher = np.array([102,255,255])
    blue_lower = np.array([94, 80, 2])
    blue_higher = np.array([126,255,255])
    
    mask = cv2.inRange(hsv_frame, blue_lower, blue_higher) 
    contours, heirarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    (h, w) = frame.shape[:2]
    frame_center_x = w // 2
    frame_center_y = h // 2
    cv2.circle(frame, (w//2, h//2), 4, (255, 255, 255), -1) 

    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area > 1000:
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.drawContours(frame, contour, -1, (0, 255, 0), 2)
            cv2.circle(frame, (cX, cY), 2, (255, 255, 255), -1)

            change_x = cX - frame_center_x 
            change_y = frame_center_y - cY
            print(change_x, change_y)
            print(area)
            dCoord = to3D(change_x,change_y,area)

            dCoordMsg = Float64MultiArray()
            dCoordMsg.data.append(dCoord[0])
            dCoordMsg.data.append(dCoord[1])
            dCoordMsg.data.append(dCoord[2])
            pub.publish(dCoordMsg)


            print("3D Coords")
            print(dCoord[0])
            print(dCoord[1])
            print(dCoord[2])

        

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(100)
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()

