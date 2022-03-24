#!/usr/bin/env python3

from __future__ import print_function
import rospy
from std_msgs.msg import Int16

from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2



# initialize the rosnode

rospy.init_node('num_people')
pub = rospy.Publisher('num_people', Int16, queue_size=10)

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--images", required=True, help="path to images directory")
#args = vars(ap.parse_args())
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
# loop over the image paths
#for imagePath in paths.list_images(args["images"]):
	# load the image and resize it to (1) reduce detection time
	# and (2) improve detection accuracy
# image = cv2.imread('Human.jpeg')
# image = imutils.resize(image, width=min(400, image.shape[1]))
# orig = image.copy()
# detect people in the image
cv2.startWindowThread()

# open webcam video stream
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('human.mp4')

# the output will be written to output.avi
out = cv2.VideoWriter(
    'output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (640,480))
while(True):
	ret,frame = cap.read()
	frame = imutils.resize(frame, width=min(400, frame.shape[1]))
	orig = frame.copy()
	(rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4), scale=1.05)
	# draw the original bounding boxes
	for (x, y, w, h) in rects:
		cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
	# draw the final bounding boxes
	person = 1
	for (xA, yA, xB, yB) in pick:
		cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
		cv2.putText(frame, f'person {person}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
		person += 1
	cv2.putText(frame, f'Total Persons : {person - 1}', (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
	print(f'TotalPerson:{person -1}')

	msg = Int16()

	msg.data = person - 1

	pub.publish(msg)

	# show some information on the number of bounding boxes
	out.write(frame.astype('uint8'))
    # Display the resulting frame
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	# show the output images
cap.release()
# and release the output
out.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)