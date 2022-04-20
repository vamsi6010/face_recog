import cv2
import numpy as np

url = "http://192.168.29.127:8080/video"

#  /video is important in ipwebcam ( live streaming ) , we can take a  photo shot by /shot.jpg

cap = cv2.VideoCapture(url)

while(True):
    camera, frame = cap.read()
    if frame is not None:
        cv2.imshow("Frame", frame)
    q = cv2.waitKey(1)
    if q==ord("q"):
        break

cv2.destroyAllWindows()