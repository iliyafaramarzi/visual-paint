import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np
import datetime


cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.8, maxHands=1)
color = (255,0,0)

canvas_image = np.zeros((480, 640, 3), np.uint8)

cx2, cy2 = 0, 0

mode = 'painting'
colors = []
with open('colors.txt') as file:
    for i in file.readlines():
        colors.append(tuple(map(int, i.replace('\n', '').split(', '))))

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

        cv2.rectangle(image, (20, 20), (100, 100), colors[0], -1)
        cv2.rectangle(image, (120, 20), (200, 100), colors[1], -1)
        cv2.rectangle(image, (220, 20), (300, 100), colors[2], -1)
        cv2.rectangle(image, (320, 20), (400, 100), colors[3], -1)
        cv2.rectangle(image, (420, 20), (500, 100), colors[4], -1)
        cv2.rectangle(image, (520, 20), (600, 100), colors[5], -1) #if you want to use eraser you should put 0,0,0 in "colors.txt" file

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
                    if 20<cx<100: color = colors[0] 
                    elif 120<cx<200: color = colors[1] 
                    elif 220<cx<300: color = colors[2]      
                    elif 320<cx<400: color = colors[3] 
                    elif 420<cx<500: color = colors[4] 
                    elif 520<cx<600: color = colors[5] 

            else:
                if color == (0,0,0):
                    cv2.line(canvas_image, (cx,cy), (cx2,cy2),color, eraser_size, -1)
                else:
                    cv2.line(canvas_image, (cx,cy), (cx2,cy2),color, brush_size, -1)

            cx2, cy2 = cx, cy

        if not fingers[0] and fingers[1] and fingers[-1] and fingers[2] and not fingers[3]:
            mode = 'painting'

        elif fingers[1] and fingers[-1] and not fingers[0] and not fingers[2] and not fingers[3]:
            mode = 'setting'
    

    gray_image = cv2.cvtColor(canvas_image, cv2.COLOR_RGB2GRAY)
    _, imageInv = cv2.threshold(gray_image, 20, 255, cv2.THRESH_BINARY_INV)
    imageInv = cv2.cvtColor(imageInv, cv2.COLOR_GRAY2BGR)
    image = cv2.bitwise_and(image, imageInv) 
    image = cv2.bitwise_or(image, canvas_image)
    cv2.imshow('main', image)
    
    if cv2.waitKey(1) == ord('s'):
        try:
            cv2.imwrite(f'Saved_files/{datetime.datetime.now().strftime("%Y %m %d %H %M %S")}.png', cv2.bitwise_or(canvas_image, imageInv))
        except:
            print('Please draw something first!')