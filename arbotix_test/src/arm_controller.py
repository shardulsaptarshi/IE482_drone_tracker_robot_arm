#!/usr/bin/env python3


#code by Shardul Nitin Saptarshi

import rospy
import math
import numpy as np
from std_msgs.msg import Float64
from std_msgs.msg import Float32


class arm_controller():
    def __init__(self,pan_angle,tilt_angle):
        
        rospy.init_node("arm_controller",anonymous=True)
        
        self.pan_angle = math.pi * pan_angle / 180            #convert degrees to rad
        self.tilt_angle = math.pi * tilt_angle / 180
        
        pan_pub = rospy.Publisher("/arm_shoulder_pan_joint/command", Float64, queue_size = 1)
        tilt_pub = rospy.Publisher("/arm_shoulder_lift_joint/command", Float64, queue_size = 1)
        
        tilt_pub.publish(self.tilt_angle)
        pan_pub.publish(self.pan_angle)

if __name__ == "__main__":

    while not rospy.is_shutdown():
        pan = np.float64(float(input("enter pan angle: ")))
        tilt = np.float64(float(input("enter tilt angle: ")))
        arm_controller(pan,tilt)
