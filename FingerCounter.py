import cv2
import random
import HandTrackingModule as htm
import time

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
"""
folderPath = "numbers"
imgNames = os.listdir(folderPath)
imgList = []

for imgPath in imgNames:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    imgList.append(image)
"""

detector = htm.HandDetector(detectionCon=0.5)

displayed_number = random.randint(1,10)
current_number = displayed_number

tipsId = [8, 12, 16, 20]
num = random.randint(1, 5)
last_correct_time = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        cv2.putText(img, str(num), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
        numFingers = []
        """
        #These are the tips of the fingers
        x4, y4 = lmList[4][1], lmList[4][2]
        x8, y8 = lmList[8][1], lmList[8][2]
        x12, y12 = lmList[12][1], lmList[12][2]
        x16, y16 = lmList[16][1], lmList[16][2]
        x20, y20 = lmList[20][1], lmList[20][2]
        #These landmarks will help us determine if our hands are open or closed.
        #If the tip of the finger is below its corresponding landmark, then that finger is closed
        x3, y3 = lmList[2][1], lmList[2][2]
        x6, y6 = lmList[6][1], lmList[6][2]
        x10, y10 = lmList[10][1], lmList[10][2]
        x14, y14 = lmList[14][1], lmList[14][2]
        x18, y18 = lmList[18][1], lmList[18][2]
        """
        #only works with one hand at the moment
        if lmList[4][1] > lmList[20][1]: #right hand
            if lmList[4][1] > lmList[3][1]:
                numFingers.append(1)
            else:
                numFingers.append(0)
        elif lmList[4][1] < lmList[20][1]: #left hand
            if lmList[4][1] < lmList[3][1]:
                numFingers.append(1)
            else:
                numFingers.append(0)

        for tip in range(0, 4):
            if lmList[tipsId[tip]][2] < lmList[tipsId[tip]-2][2]:
                numFingers.append(1)
            else:
                numFingers.append(0)

        finger_count = 0
        for i in numFingers:
            if i == 1:
                finger_count += 1


        # only do this when the number of fingers matches the current number
        if finger_count == num:
            cv2.putText(img,"Correct", (200, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (0, 255, 0), 3)
            if time.time() - last_correct_time >= 2:
                last_correct_time = time.time()
                num = random.randint(1, 5)
                cv2.putText(img, str(num), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                            (255, 0, 255), 3)




    cv2.imshow("Image", img)
    cv2.waitKey(1)
