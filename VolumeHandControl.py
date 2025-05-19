import cv2
import numpy as np
import time
import HandTrackingModule as htm

cap = cv2.VideoCapture(0) #Video Object
wCam, hCam = 640, 480 #custom video width and height
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7) #initialize hand detection object

while True:
    success,img = cap.read() #img actually consists of a numpy array with pixel and BGR value
    flipped_img = cv2.flip(img, 1)
    img = detector.findHands(flipped_img) #return a img with handlms points drawn
    lmlist = detector.findPosition(img, draw = False) #all landmark points for 1 hand
    '''
        Extracting landmark for index tip and thumb tip:
        highlighting the points with circle shape
        and creating a line between them with line shape
    '''
    if(len(lmlist) != 0):
        print(lmlist[4], lmlist[8])

        x1, y1 = lmlist[4][1] , lmlist[4][2]
        x2, y2 = lmlist[8][1] , lmlist[8][2]
        cx,cy = (x1+x2)//2 , (y1+y2)//2 #find midpoint of line

        cv2.circle(img , (x1, y1), 10 , (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,255,255), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {str(int(fps))}', (40,50), cv2.FONT_HERSHEY_SIMPLEX, 1
                , (255, 0, 0) , 3)



    cv2.imshow("Image", img)
    cv2.waitKey(1)