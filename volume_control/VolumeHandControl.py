import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import osascript
import AppKit

wCam, hCam = 640, 480 #width and height



cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.HandDetector(detectionCon = 0.5) #creates an object of the class HandDetector

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False) #creates a list with all of the positions from the different landmarks
    #index finger(lm 8) and thumb (lm 4) used for volume selector
    if len(lmList) != 0:
        x4, y4 = lmList[4][1], lmList[4][2]
        x8, y8 = lmList[8][1], lmList[8][2]
        #drawing a circle on the two necessary fingers and a line inbetween:
        cv2.circle(img, (x4, y4), 10, (255,0, 0), cv2.FILLED)
        cv2.circle(img, (x8, y8), 10, (255,0, 0), cv2.FILLED)
        cv2.line(img, (x4, y4), (x8, y8), (255,0, 0), 5)
        lineLen = math.hypot(x8-x4, y8-y4)

        if lineLen < 27:
            volume = 0
            vol = "set volume output volume " + str(volume)
            osascript.osascript(vol)
        else:
            volume = np.interp(lineLen, [27,310], [0,283])
            vol = "set volume output volume " + str(volume)
            osascript.osascript(vol)



    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS{int(fps)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)


    cv2.imshow("Image", img)
    cv2.waitKey(1)