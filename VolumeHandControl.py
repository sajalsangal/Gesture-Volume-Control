import cv2
import numpy as np
import time
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

while True:
    success,img = cap.read()
    flipped_img = cv2.flip(img, 1)
    img = detector.findHands(flipped_img)
    lmlist = detector.findPosition(img, draw = False)
    if(len(lmlist) != 0):
        print(lmlist[4], lmlist[8])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {str(int(fps))}', (40,50), cv2.FONT_HERSHEY_SIMPLEX, 1
                , (255, 0, 0) , 3)



    cv2.imshow("Image", img)
    cv2.waitKey(1)