#!/usr/bin/env python3

#original code by SowmiyaNarayanan G and SowmiyaNarayanan G. Link: https://github.com/GSNCodes/ArUCo-Markers-Pose-Estimation-Generation-Python
#modifications by Shardul Nitin Saptarshi

import numpy as np
import cv2
#import yaml


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

cap = cv2.VideoCapture(0)
num = 10
found = 0
while(found < num):  # Here, 10 can be changed to whatever number you like to choose
    ret, img = cap.read() # Capture frame-by-frame
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,6), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)  # Certainly, every loop objp is the same, in 3D.

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7,6), corners2, ret)

        # Enable the following 2 lines if you want to save the calibration images.
        # filename = str(found) +".jpg"
        # cv2.imwrite(filename, img)

        found += 1

    cv2.imshow('img', img)
    cv2.waitKey(10)


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

np.save("calibration_matrix", mtx)
np.save("distortion_coefficients", dist)

#  Python code to write the image (OpenCV 3.2)
fs = cv2.FileStorage('calibration.yml', cv2.FILE_STORAGE_WRITE)
fs.write('camera_matrix', mtx)
fs.write('dist_coeff', dist)
fs.release()



# If you want to use PyYAML to read and write yaml files,
# try the following part
# It's very important to transform the matrix to list.
# data = {'camera_matrix': np.asarray(mtx).tolist(), 'dist_coeff': np.asarray(dist).tolist()}

# with open("calibration.yaml", "w") as f:
#    yaml.dump(data, f)

# You can use the following 4 lines of code to load the data in file "calibration.yaml"
# Read YAML file
#with open(calibrationFile, 'r') as stream:
#    dictionary = yaml.safe_load(stream)
#camera_matrix = dictionary.get("camera_matrix")
#dist_coeffs = dictionary.get("dist_coeff")