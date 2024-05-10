#!/usr/bin/env python3

import rospy
import math
import numpy as np
from std_msgs.msg import Float64

pan_offset = 0
tilt_offset = -90

class arm_controller():
    def __init__(self,target_point):
        
        rospy.init_node("arm_controller",anonymous=True)

        pan_pub = rospy.Publisher("/arm_shoulder_pan_joint/command", Float64, queue_size = 1)
        tilt_pub = rospy.Publisher("/arm_shoulder_lift_joint/command", Float64, queue_size = 1)
        
        #arm origin coordinates in free space (m)
        point1 = (0,0,0)
        self.line_to_angles(point1, target_point)
        print(f"writing angles tilt = {np.degrees(self.tilt_angle)} and pan = {np.degrees(self.pan_angle)}")
        tilt_pub.publish(self.tilt_angle + np.radians(tilt_offset))
        pan_pub.publish(self.pan_angle + np.radians(pan_offset))



    #code from ChatGPT. prompt: how to convert 2 point 3d line to azimuth and polar angle representation
    def line_to_angles(self, point1, point2):
        # Calculate direction vector
        v = np.array(point2) - np.array(point1)
        
        # Azimuthal angle (phi)
        phi = np.arctan2(v[1], v[0])   
        # Polar angle (theta)
        theta = np.arccos(v[2] / np.linalg.norm(v))

        self.pan_angle = phi 
        self.tilt_angle = theta


if __name__ == "__main__":

    while not rospy.is_shutdown():
        # pan = np.float64(float(input("enter pan angle: ")))
        # tilt = np.float64(float(input("enter tilt angle: ")))

        tx = np.float64(float(input("enter the target x position ")))
        ty = np.float64(float(input("enter the target y position ")))
        tz = np.float64(float(input("enter the target z position ")))

        target_point = (tx,ty,tz)

        arm_controller(target_point)
