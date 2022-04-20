import cv2
import numpy as np

cap = cv2.VideoCapture(0)
tracker = cv2.legacy.TrackerMOSSE_create()
tracker = cv2.legacy.TrackerCSRT_create()

success, img = cap.read()

bbox = cv2.selectROI("Tracking", img, False)

tracker.init(img, bbox)

def drawBox(img,bbox):
    x,y,w,h= int(bbox[0]) , int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)
    cv2.putText(img, "Hi  ,I am Tracking You", (95, 75), cv2.FONT_HERSHEY_COMPLEX, 0.9, (100, 255, 22))


while True:
    timer = cv2.getTickCount()
    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)

    success , img  = cap.read()
    success , bbox = tracker.update(img)

    if success:
        drawBox(img, bbox)
    else:
        cv2.putText(img, "I Lost you , Any one here ?", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255))

    cv2.putText(img,str(int(fps)),(85,50),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255))
    cv2.imshow("Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

