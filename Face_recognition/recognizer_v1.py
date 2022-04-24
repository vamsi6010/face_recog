import cv2
import numpy as np
import os

from collections import namedtuple



RECT_NAMEDTUPLE = namedtuple('RECT_NAMEDTUPLE', 'x1 x2 y1 y2')


def overlap(rec1, rec2):
    x ,y, w , h , x_, y_ ,w_,h_ = int(rec1.x1 ), int(rec1.x2), int(rec1.y1),int( rec1.y2), int(rec2.x1),int(rec2.x2), int(rec2.y1),int(rec2.y2)
    print(x ,y, w , h , x_, y_ ,w_,h_)
    if not len(set(range(x, x + w)) & set(range(x_, x_ + w_))) == 0 and \
            not len(set(range(y, y + h)) & set(range(y_, y_ + h_))) == 0:
        return True
    else:
        return False
    # if (rec2.x2 > rec1.x1 and rec2.x2 < rec1.x2) or \
    #         (rec2.x1 > rec1.x1 and rec2.x1 < rec1.x2):
    #     x_match = True
    # else:
    #     x_match = False
    # if (rec2.y2 > rec1.y1 and rec2.y2 < rec1.y2) or \
    #         (rec2.y1 > rec1.y1 and rec2.y1 < rec1.y2):
    #     y_match = True
    # else:
    #     y_match = False
    # if x_match and y_match:
    #     return True
    # else:
    #     return False


def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
    cv2.putText(img, "Hi  ,I am Tracking You", (95, 75), cv2.FONT_HERSHEY_COMPLEX, 0.9, (100, 255, 22))


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX
# iniciate id counter
id = 0
# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'vamsi', 'jeff', "Arul Shakthi HQ", "Dinesh-Babu", 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, "Nandha - Marketer"]
# Initialize and start realtime video capture


tracker = cv2.legacy.TrackerMOSSE_create()
# tracker = cv2.legacy.TrackerCSRT_create()
cap = cv2.VideoCapture("http://10.42.0.132:8080/video")

success, img = cap.read()

bbox1 = cv2.selectROI("Tracking", img, False)
# bbox1 = bbox.copy()
# img1 = img.copy()

Rect1 = RECT_NAMEDTUPLE(bbox1[0],bbox1[1],bbox1[2],bbox1[3] )
bbox = cv2.selectROI("object needed", img, False)
print(type(bbox), bbox)
# can we select roi from
tracker.init(img, bbox)

cam = cv2.VideoCapture("http://10.42.0.132:8080/video")
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height
# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

cam1 = cv2.VideoCapture("http://10.42.0.80:8080/video")
cam1.set(3, 640)  # set video widht
cam1.set(4, 480)  # set video height
# Define min window size to be recognized as a face
minW1 = 0.1 * cam1.get(3)
minH1 = 0.1 * cam1.get(4)

while True:
    # Rect2 = RECT_NAMEDTUPLE(20, 210, 10, 60)

    # drawBox(img, bbox1)

    # print("Overlap found?", overlap(bbox, Rect2))
    timer = cv2.getTickCount()
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    ret, img = cam.read()
    drawBox(img, bbox1)
    ret, bbox = tracker.update(img)

    Rect2 = RECT_NAMEDTUPLE(bbox[0],bbox[1],bbox[2],bbox[3])

    if ret:
        drawBox(img, bbox)
    else:
        cv2.putText(img, "I Lost you , Any one here ?", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255))
    if overlap(Rect2, Rect1):
        print("O`verlap found" )
    cv2.putText(img, str(int(fps)), (85, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255))
    cv2.imshow("Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # If confidence is less them 100 ==> "0" : perfect match
        if (confidence < 100):
            print(id)
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(
            img,
            str(id),
            (x + 5, y - 5),
            font,
            1,
            (255, 255, 255),
            2
        )
        cv2.putText(
            img,
            str(confidence),
            (x + 5, y + h - 5),
            font,
            1,
            (255, 255, 0),
            1
        )

    cv2.imshow('camera', img)
    ret1, img1 = cam1.read()

    img1 = cv2.flip(img1, 1)
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW1), int(minH1)),
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # If confidence is less them 100 ==> "0" : perfect match
        if (confidence < 100):
            print(id)
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(
            img1,
            str(id),
            (x + 5, y - 5),
            font,
            1,
            (255, 255, 255),
            2
        )
        cv2.putText(
            img1,
            str(confidence),
            (x + 5, y + h - 5),
            font,
            1,
            (255, 255, 0),
            1
        )

    cv2.imshow('camera', img1)

    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()

cv2.destroyAllWindows()
