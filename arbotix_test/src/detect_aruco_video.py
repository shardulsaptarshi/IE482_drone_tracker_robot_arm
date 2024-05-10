#!/usr/bin/env python3



#original code by SowmiyaNarayanan G and SowmiyaNarayanan G. Link: https://github.com/GSNCodes/ArUCo-Markers-Pose-Estimation-Generation-Python
#modifications by Shardul Nitin Saptarshi

'''
Sample Command:-
python detect_aruco_video.py --type DICT_5X5_100 --camera True
python detect_aruco_video.py --type DICT_5X5_100 --camera False --video test_video.mp4
'''

import numpy as np
from utils import ARUCO_DICT, aruco_display
import argparse
import time
import cv2
import sys
import rospy
from std_msgs.msg import Int32MultiArray


def detect_aruco_video():
	


	#inintialize ROS node
	rospy.init_node("detect_aruco_video", anonymous=True)
	pub = rospy.Publisher('/aruco_coords', Int32MultiArray, queue_size=1)
	rate = rospy.Rate(20)

	#make an array to store the aruco coordinates
	coords = Int32MultiArray()

	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--camera", required=True, help="Set to True if using webcam")
	ap.add_argument("-v", "--video", help="Path to the video file")
	ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="Type of ArUCo tag to detect")
	args = vars(ap.parse_args())


	if args["camera"].lower() == "true":
		video = cv2.VideoCapture(0)
		time.sleep(2.0)


	else:
		if args["video"] is None:
			print("[Error] Video file location is not provided")
			sys.exit(1) 

		video = cv2.VideoCapture(args["video"])

	if ARUCO_DICT.get(args["type"], None) is None:
		print(f"ArUCo tag type '{args['type']}' is not supported")
		sys.exit(0)

	arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
	arucoParams = cv2.aruco.DetectorParameters_create()

	ret, frame = video.read()
	h, w, _ = frame.shape 
	x =  int(w/2)
	y = int(h/2)

	while not rospy.is_shutdown():
		
		ret, frame = video.read()
		#frame = cv2.flip(frame, 1)  #flip the frame (and hence video) horizontally.

		if ret is False:
			break

		h, w, _ = frame.shape  	#dimensions of the image

		# width = 1000
		# height = int(width*(h/w))

		width = w
		height = h

		frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)
		corners, ids, rejected = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

		detected_markers,x,y = aruco_display(corners, ids, rejected, frame,h,w,x,y)
		#x and y are both 500, when there is no tag detected.


		cv2.imshow("Image", detected_markers)

		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break 
 
		
		coords.data = [x,y,h,w]			#we are sending the resolution of the camera also
		pub.publish(coords)
		rate.sleep()

	cv2.destroyAllWindows()
	video.release()


if __name__ == "__main__":
	detect_aruco_video()