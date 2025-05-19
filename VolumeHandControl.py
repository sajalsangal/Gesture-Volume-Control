import cv2
import mediapipe as mp
import numpy as np
import time

cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

while True:
    success,img = cap.read()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    flipped_img = cv2.flip(img,1)
    cv2.putText(flipped_img, f'FPS: {str(int(fps))}', (40,50), cv2.FONT_HERSHEY_SIMPLEX, 1
                , (255, 0, 0) , 3)
    cv2.imshow("Image", flipped_img)
    cv2.waitKey(1)