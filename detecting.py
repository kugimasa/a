import cv2
import numpy as np
from skimage.io import imread, imsave

def nothing(x):
    pass

def anime_filter(img):
    # change to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    # blur
    edge = cv2.blur(gray, (3, 3))
    # Canny edge
    edge = cv2.Canny(edge, 50, 150, apertureSize=3)
    # change to RGB
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
    
    img = cv2.pyrMeanShiftFiltering(img, 5, 20)
  
    return cv2.subtract(img, edge)


cv2.namedWindow('video image')

# create switch for ON/OFF functionality
switch = 'change_face'
cv2.createTrackbar(switch, 'video image',0,1,nothing)
manga = 'manga'
cv2.createTrackbar(manga, 'video image',0,1,nothing)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
im = imread('face.jpg')
cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    
    
    s = cv2.getTrackbarPos(switch,'video image')
    m = cv2.getTrackbarPos(manga,'video image')
    if s == 1:
        for x, y, w, h in faces:
            face = img[y: y + h, x: x + w]
            im_resize = cv2.resize(im,(w, h))
            img[y: y + h, x: x + w] = im_resize
    if m == 1:
        img = anime_filter(img)
    
    cv2.imshow('video image', img)
    key = cv2.waitKey(10)
    if key == 27:  # ESCキーで終了
        break

cap.release()
cv2.destroyAllWindows()
