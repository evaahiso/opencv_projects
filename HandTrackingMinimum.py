import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0) #selects camera

mpHands = mp.solutions.hands #refer to hands.py documentation
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0 #previous
cTime = 0 #current

while True:
    success, img = cap.read() #gives us the frame
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #check if there are multiple hands
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h) #gets the pixels where the landmark is at the moment
                if id == 0:
                    cv2.circle(img, (cx,cy), 25, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) #handLms is a single hand, draw_landmarks draws red points at main hand lms
            #these landmarks can be tracked to monitor a particular position/hand movement

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)