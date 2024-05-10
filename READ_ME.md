Project: Drone Tracking Robot Arm


Goal
A drone tracking robot arm. The physical arm will be constructed using the AX-12A servos, "Trossen" robot package. Computer vision will be used to track the movement of a drone with onboard aruco tags, and the arm will reposition itself so that it 
is pointing towards the drone.
Stretch goals:
1)	Introduce control mechanism: voice control using AI powered live transcription.
2)  Develop control system to stabilize the robot arm movement


Impact

This will augment the human ability to record video footage of fast moving objects from one place to another, thereby improving safety and efficiency in many industrial scenarios and beyond.

Technical Plan 
1)	Arduino along with an external power source will be used to manually control servo motors for initial testing. 
    a.  Python could read and write serial data to the Arduino to control the robot arm using ROS.
    b.	Alternatively, a raspberry pi can be used instead of Arduino to directly run ROS in the robot arm. 
2)	Python, and the OpenCV library will be used to track an aruco tag and convert motion into control commands for the robot.
3)	Whisper AI could be used for transcription.
YouTube link: https://www.youtube.com/watch?v=iefxCFcSns8
https://www.youtube.com/watch?v=f2TUxoaKIsA


Milestones/high-level timeline 

Over spring break: 
1)	Acquire all required hardware components. 
2)	Assemble and manually test individual servo motors. 
Week 1:
-Get familiarized with open CV functions.
Week 2:
-Start building basic ibject tracking framework in OpenCV.
Week 3:
-Start building basic object tracking framework in OpenCV.
-Calibrate aruco tags
Week 4:
-Develop algorithms to map OpenCV output to servo motor commands.
Week 5:
1)	Optimize robotic arm stability.
Week 6:
1)	Introduce voice command high level control.
2)	Resolve any bugs.
3)	Create a visual demo of the project.
