import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np


cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.8, maxHands=1)
color = 255,0,0

canvas_image = np.zeros((480, 640, 3), np.uint8)

cx2, cy2 = 0, 0

mode = 'painting'

x_brush, y_brush = 60, 100
x_eraser, y_eraser = 60, 300
brush_size = 7
eraser_size = 7
while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    hands = detector.findHands(image, draw=False)
    if hands != []:
        lmList = hands[0]['lmList']
    else:
        lmList = hands
    
    if mode == 'painting':
        Blue = cv2.imread('Pictures/Blue.png', cv2.IMREAD_COLOR)
        image[20:100, 20:100] = 0
        image[20:100, 20:100] += Blue

        Green = cv2.imread('Pictures/Green.png', cv2.IMREAD_COLOR)
        image[20:100, 120:200] = 0
        image[20:100, 120:200] += Green

        Yellow = cv2.imread('Pictures/Yellow.png', cv2.IMREAD_COLOR)
        image[20:100, 220:300] = 0
        image[20:100, 220:300] += Yellow

        Red = cv2.imread('Pictures/Red.png', cv2.IMREAD_COLOR)
        image[20:100, 320:400] = 0
        image[20:100, 320:400] += Red
        
        White = cv2.imread('Pictures/White.png', cv2.IMREAD_COLOR)
        image[20:100, 420:500] = 0
        image[20:100, 420:500] += White

        eraser = cv2.imread('Pictures/eraser.jpg', cv2.IMREAD_COLOR)
        image[20:100, 520:600] = 0
        image[20:100, 520:600] += eraser

    else:
        cv2.rectangle(image, (50,100), (600, 104), (100,100,100), -1)
        cv2.rectangle(image, (50,300), (600, 304), (100,100,100), -1)
        cv2.putText(image, 'brush size: %i' % brush_size, (50,80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        cv2.putText(image, 'eraser size: %i' % eraser_size, (50,280), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))

        if x_brush >= 590: x_brush = 590
        if x_brush <= 60: x_brush = 60
        if x_eraser >= 590: x_eraser = 590
        if x_eraser <= 60: x_eraser = 60

        brush_size = int(np.interp(x_brush, [60, 590], [3, 30]))
        eraser_size = int(np.interp(x_eraser, [60, 590], [3, 30]))

        cv2.circle(image, (x_brush,100), 10, (200,200,200), -1)
        cv2.circle(image, (x_eraser,300), 10, (200,200,200), -1)

        if lmList:
            cv2.circle(image, lmList[8][:-1], 10, (50,50,50))
            cv2.circle(image, lmList[12][:-1], 10, (50,50,50))
            l, _ = detector.findDistance(lmList[8][:-1], lmList[12][:-1])
            if l < 40:
                cursor = lmList[8]
                w, h = 40, 40   
                if x_brush-w<cursor[0]<x_brush+w and y_brush-h<cursor[1]<y_brush+h:
                    x_brush, y_brush = lmList[8][:-1]
                if x_eraser-w<cursor[0]<x_eraser+w and y_eraser-h<cursor[1]<y_eraser+h:
                    x_eraser, y_eraser = lmList[8][:-1]
        
        cx2, cy2 = 0, 0
    
    if lmList:
        l, _ = detector.findDistance(lmList[8][:-1], lmList[12][:-1])
        fingers = detector.fingersUp(hands[0])
        
        if mode == 'painting':
            cx, cy = lmList[8][:-1]
            if cx2 == 0 and cy2 == 0:
                cx2, cy2 = cx, cy
            cv2.circle(image, (cx,cy), 7, color, -1)
            fingersup = detector.fingersUp(hands[0])
            if l<35 and fingersup[1] == 1 and fingersup [2] == 1:
                if 20<cy<100:
                    cx2, cy2 = cx, cy

                    # RGB BGR 
                    if 20<cx<100: color = (255, 0, 0) #blue 
                    elif 120<cx<200: color = (0, 255, 0) #green 
                    elif 220<cx<300: color = (0, 255, 255) #yellow 255 255 0, 255     
                    elif 320<cx<400: color = (0, 0, 255) # red
                    elif 420<cx<500: color = (255,255,255) # white
                    elif 520<cx<600: color = (0,0,0) #eraser

            else:
                if color == (0,0,0):
                    cv2.line(canvas_image, (cx,cy), (cx2,cy2),color, eraser_size, -1)
                else:
                    cv2.line(canvas_image, (cx,cy), (cx2,cy2),color, brush_size, -1)

            cx2, cy2 = cx, cy

            gray_image = cv2.cvtColor(canvas_image, cv2.COLOR_RGB2GRAY)
            _, imageInv = cv2.threshold(gray_image, 20, 255, cv2.THRESH_BINARY_INV)
            imageInv = cv2.cvtColor(imageInv, cv2.COLOR_GRAY2BGR)
            image = cv2.bitwise_and(image, imageInv) 
            image = cv2.bitwise_or(image, canvas_image)

        if not fingers[0] and fingers[1] and fingers[-1] and fingers[2] and not fingers[3]:
            mode = 'painting'

        elif fingers[1] and fingers[-1] and not fingers[0] and not fingers[2] and not fingers[3]:
            mode = 'setting'
    


    cv2.imshow('main', image)
    cv2.waitKey(1)