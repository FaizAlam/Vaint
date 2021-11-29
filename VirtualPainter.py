import numpy as np
import os
import time
import cv2
import HandTrackingModule as htm


folderPath = 'header'
myList = os.listdir(folderPath)
print(myList)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))


#######################
brushThickness = 15
xp,yp = 0,0
header = overlayList[-1]
drawColor = (0,255,0)
eraserThickness = 50
#######################

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
imgCanvas = np.zeros((720,1280,3),np.uint8)

detector = htm.handDetector(detectionCon=0.75)
while True:
    # 1. Import image
    success,img = cap.read() 
    img = cv2.flip(img,1)   # fliping to avoid left right issue

    # 2. Find Hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)

    if len(lmList)!=0:
        
        #print(lmList)
        #tip of index and middle fingers
        x1,y1 = lmList[8][1:]   
        x2,y2 = lmList[12][1:]
        # 3. Check which fingers are up
        fingers = detector.fingersUp()

        # 4. If selection mode ( two fingers are up ) - select
        if fingers[1] and fingers[2]:
            xp,yp = 0,0
            #print("selection mode")
            if y1 < 120: # check if in the header
                if 350<x1<550:  #check if first color selected
                    header = overlayList[-1]
                    drawColor = (0,255,0)       #green
                elif 600<x1<750:
                    header = overlayList[-3]
                    drawColor = (0,255,255)     #yellow
                elif 800< x1<910:
                    header = overlayList[-2]
                    drawColor = (255,0,255)     #purple
                elif 1000<x1<1150:
                    header = overlayList[-4]
                    drawColor = (0,0,0)

            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)


        # 5. If drawing mode ( index finger is up) - draw
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            #print("drawing mode")
            if xp==0 and yp==0:
                xp,yp = x1,y1

            if drawColor == (0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)
            xp,yp = x1,y1

    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)

    #setting the header image
    img[0:120,0:1280] = header
    #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Vaint",img)
    #cv2.imshow("Canvas",imgInv)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()

