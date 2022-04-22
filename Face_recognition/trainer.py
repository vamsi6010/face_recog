import cv2
import numpy as np
from PIL import Image
import os
path = 'dataset'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
def getImagesAndLabels():
    # Path for face image database
    # function to get the images and label data
    print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    print(imagePaths)
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return face_trainer(faceSamples,ids)

def face_trainer(faces,ids):
    recognizer.train(faces, np.array(ids))
    # Save the model into trainer/trainer.yml
    recognizer.write('trainer/trainer.yml')
    # Print the numer of faces trained and end program
    return print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))


# getImagesAndLabels()