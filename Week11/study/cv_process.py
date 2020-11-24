#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: cv_process.py
#@Software: PyCharm


import cv2
import os
# Opens the Video file
cap= cv2.VideoCapture('../data/snow.mp4')
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break

    img_file = "../data/mp4_img"
    if not os.path.exists(img_file):
        os.mkdir(img_file)
    cv2.imwrite(img_file + "/" + str(i) + '.jpg', frame)

    i += 1

cap.release()
cv2.destroyAllWindows()