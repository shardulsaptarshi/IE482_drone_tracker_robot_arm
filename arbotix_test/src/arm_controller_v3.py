#!/usr/bin/env python3


#code by Shardul Nitin Saptarshi
#references: Rizky Dermawan, "face detection" link: https://github.com/rizkydermawan1992/face-detection

import rospy
import math
import numpy as np
from std_msgs.msg import Float64
from std_msgs.msg import Float32
from std_msgs.msg import Int32MultiArray



class arm_controller():
    def __init__(self):

        self.error_pan_sum = 0
        self.error_tilt_sum = 0

        rospy.init_node("arm_controller",anonymous=True)
        
        self.pan_angle = 90            #setting default servo angles, converting degrees to rad
        self.tilt_angle = 0
        
        self.pan_pub = rospy.Publisher("/arm_shoulder_pan_joint/command", Float64, queue_size = 1)
        self.tilt_pub = rospy.Publisher("/arm_shoulder_lift_joint/command", Float64, queue_size = 1)

        rospy.Subscriber("/aruco_coords", Int32MultiArray, self.callback_tagloc)
        rospy.spin()

    def callback_tagloc(self,msg):
        



        aruco_w, aruco_h = msg.data[0], msg.data[1]
        
        h = msg.data[2]                   #resolution width of the video stream
        w = msg.data[3]                   #resolution height of the video stream
        
        #the code below is specifically for the servos in the arbotix robot
        #in the robots current assembly, 
        
        #TILT: servo angle decreases upwards
        #min tilt angle: -150 deg
        #max tilt angle: 45 deg

        #PAN: servo andle decreases to the right of the robot
        #min tilt angle: -60 deg
        #max pan angle: 240 deg

        wm  = int(w/2)
        hm = int(h/2)

        Pw = 0.4           #proportional gains
        Ph = 0.4

        Iw = 0.002           #integral gains
        Ih = 0.002




        error_pan = abs(wm - aruco_w) * 0.1
        self.error_pan_sum = self.error_pan_sum + error_pan
        
        error_tilt = abs(hm - aruco_h) * 0.1
        self.error_tilt_sum = self.error_tilt_sum + error_tilt

        if wm > aruco_w:    #case 1
            self.pan_angle = self.pan_angle + Pw * error_pan 

        elif wm < aruco_w:    #case 2
            self.pan_angle = self.pan_angle - Pw * error_pan

        if hm > aruco_h:    #case 1
            self.tilt_angle = self.tilt_angle - Ph * error_tilt 

        elif hm < aruco_h:    #case 2
            self.tilt_angle = self.tilt_angle + Ph * error_tilt 




        self.tilt_angle = max(self.tilt_angle,-150)
        self.tilt_angle = min(self.tilt_angle,45)

        self.pan_angle = max(self.pan_angle,-60)
        self.pan_angle = min(self.pan_angle,240)

        print(f"error tilt =  {error_tilt} and error pan = {error_pan}")
        print(f"writing tilt =  {self.tilt_angle} and pan = {self.pan_angle}")


        self.pan_angle = math.pi * self.pan_angle / 180
        self.tilt_angle = math.pi * self.tilt_angle / 180

        self.tilt_pub.publish(self.tilt_angle)
        self.pan_pub.publish(self.pan_angle)

        pass


if __name__ == "__main__":
    arm_controller()
