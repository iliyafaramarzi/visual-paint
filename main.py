import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.8)
color = 255,0,0

canvas_image = np.zeros((480, 640, 3), np.uint8)

cx2, cy2 = 0, 0
while True:
    success, image = cap.read()
    image = detector.findHands(image, False)
    lmList, _  = detector.findPosition(image, draw=False)
    cv2.rectangle(image, (50,50), (150,150), (255,0,0), -1)
    cv2.rectangle(image, (200,50), (300,150), (0,255,0), -1)
    cv2.rectangle(image, (350,50), (450,150), (0,0,255), -1)
    cv2.rectangle(image, (500,50), (600,150), (0,0,0), -1)



    if lmList:

        l, _, _ = detector.findDistance(8, 12, image, draw=False)
        cx, cy = lmList[8]
        if cx2 == 0 and cy2 == 0:
            cx2, cy2 = cx, cy
        cv2.circle(image, (cx,cy), 7, color, -1)
        fingersup = detector.fingersUp()
        if l<30 and fingersup[1] == 1 and fingersup[2] == 1:
            if 50<cy<150:
                cx2, cy2 = 0, 0
                if 50<cx<150: color = 255,0,0                    
                elif 200<cx<300: color = 0,255,0
                elif 350<cx<450: color = 0,0,255
                elif 500<cx<600: color = 0,0,0
        else:
            if color == (0,0,0):
                cv2.line(canvas_image, (cx,cy), (cx2,cy2),color, 30, -1)
            else:
                cv2.line(canvas_image, (cx,cy), (cx2,cy2),color, 7, -1)

        cx2, cy2 = cx, cy
    
    gray_image = cv2.cvtColor(canvas_image, cv2.COLOR_RGB2GRAY)
    _, imageInv = cv2.threshold(gray_image, 20, 255, cv2.THRESH_BINARY_INV)
    imageInv = cv2.cvtColor(imageInv, cv2.COLOR_GRAY2BGR)
    image = cv2.bitwise_and(image, imageInv) 
    image = cv2.bitwise_or(image, canvas_image) 

    cv2.imshow('main', image)
    # cv2.imshow('canvas image', canvas_image)
    cv2.waitKey(1)