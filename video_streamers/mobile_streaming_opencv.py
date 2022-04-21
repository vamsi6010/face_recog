# import cv2
# import numpy as np
#
# url = "http://192.168.100.52:8080/video"
#
#
# #  /video is important in ipwebcam ( live streaming ) , we can take a  photo shot by /shot.jpg
#
# cap = cv2.VideoCapture(url)
#
# while(True):
#     camera, frame = cap.read()
#     if frame is not None:
#         cv2.imshow("Frame", frame)
#     q = cv2.waitKey(1)
#     if q==ord("q"):
#         break
#
# cv2.destroyAllWindows()


import cv2

frame0 = cv2.VideoCapture("http://192.168.100.52:8080/video")
frame1 = cv2.VideoCapture("http://192.168.100.184:8080/video")
while 1:

   ret0, img0 = frame0.read()
   ret1, img00 = frame1.read()
   img1 = cv2.resize(img0,(360,240))
   img2 = cv2.resize(img00,(360,240))
   if (frame0):
       cv2.imshow('img1',img1)
   if (frame1):
       cv2.imshow('img2',img2)

   k = cv2.waitKey(30) & 0xff
   if k == 27:
      break

frame0.release()
frame1.release()
cv2.destroyAllWindows()