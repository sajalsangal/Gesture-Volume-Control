import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0) #Video Object
wCam, hCam = 640, 480 #custom video width and height
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(detectionCon=0.7) #initialize hand detection object

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-5.0, None)
minVol = volRange[0]
maxVol = volRange[1]



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

        x1, y1 = lmlist[4][1] , lmlist[4][2]
        x2, y2 = lmlist[8][1] , lmlist[8][2]
        cx,cy = (x1+x2)//2 , (y1+y2)//2 #find midpoint of line

        cv2.circle(img , (x1, y1), 10 , (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,255,255), 3)
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        length = int(math.hypot(x2 - x1 , y2 - y1)) #find length of line from x and y coordinates
        #print(length)


        # hand range is from 30 - 150
        # volume range is from -65 - 0

        vol = np.interp(length, [30,150], [minVol, maxVol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 30: #When fingers come close
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED) #change the color of the midpoint to give a button effect


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {str(int(fps))}', (40,50), cv2.FONT_HERSHEY_SIMPLEX, 1
                , (255, 0, 0) , 3)



    cv2.imshow("Image", img)
    cv2.waitKey(1)