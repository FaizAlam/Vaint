import cv2
import numpy as np
import os
import HandTrackingModule as htm

class VideoCamera():
    def __init__(self,overlay_image=[],draw_color=(0,255,0)):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,1280)
        self.cap.set(4,720)
        self.xp = 0
        self.yp = 0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.brush_thickness = 15
        self.eraser_thickness = 75
        self.overlay_image = overlay_image
        self.draw_color = draw_color
        self.detector = htm.handDetector(detectionCon=0.85)
        self.image_canvas = np.zeros((720,1280,3),np.uint8)
        self.default_overlay = overlay_image[-1]
    
    def __del__(self):
        self.cap.release()
    
    def set_overlay(self,frame,overlay_image):
        self.default_overlay = overlay_image[-1]
        
        frame[0:120,0:1280] = self.default_overlay
        return frame
    
    def get_frame(self,overlay_image):
        _,frame = self.cap.read()
        frame = cv2.flip(frame,1)
        frame[0:120,0:1280] = self.default_overlay
        
        img = self.detector.findHands(frame,draw=True)
        lmList = self.detector.findPosition(img,draw=False)

        if len(lmList)!=0:
        
            #print(lmList)
            #tip of index and middle fingers
            self.x1,self.y1 = lmList[8][1:]   
            self.x2,self.y2 = lmList[12][1:]
            # 3. Check which fingers are up
            fingers = self.detector.fingersUp()

            # 4. If selection mode ( two fingers are up ) - select
            if fingers[1] and fingers[2]:
                self.xp,self.yp = 0,0
                #print("selection mode")
                if self.y1 < 120: # check if in the header
                    if 350<self.x1<550:  #check if first color selected
                        self.default_overlay = overlay_image[-1]
                        img[0:120,0:1280] = self.default_overlay
                        self.draw_color = (0,255,0)       #green
                    elif 600<self.x1<750:
                        self.default_overlay = overlay_image[-3]
                        img[0:120,0:1280] = self.default_overlay
                        self.draw_color = (0,255,255)     #yellow
                    elif 800<self.x1<910:
                        self.default_overlay = overlay_image[-2]
                        img[0:120,0:1280] = self.default_overlay
                        self.draw_color = (255,0,255)     #purple
                    elif 1000<self.x1<1150:
                        self.default_overlay = overlay_image[-4]
                        img[0:120,0:1280] = self.default_overlay
                        self.draw_color = (0,0,0)

                cv2.rectangle(img,(self.x1,self.y1-25),(self.x2,self.y2+25),self.draw_color,cv2.FILLED)


            # 5. If drawing mode ( index finger is up) - draw
            if fingers[1] and fingers[2]==False:
                cv2.circle(img,(self.x1,self.y1),15,self.draw_color,cv2.FILLED)
                #print("drawing mode")
                if self.xp==0 and self.yp==0:
                    self.xp,self.yp = self.x1,self.y1

                if self.draw_color == (0,0,0):
                    cv2.line(img,(self.xp,self.yp),(self.x1,self.y1),self.draw_color,self.eraser_thickness)
                    cv2.line(self.image_canvas,(self.xp,self.yp),(self.x1,self.y1),self.draw_color,self.eraser_thickness)
                else:
                    cv2.line(img,(self.xp,self.yp),(self.x1,self.y1),self.draw_color,self.brush_thickness)
                    cv2.line(self.image_canvas,(self.xp,self.yp),(self.x1,self.y1),self.draw_color,self.brush_thickness)
                self.xp,self.yp = self.x1,self.y1
        

        img[0:120,0:1280] = self.default_overlay
        imgGray = cv2.cvtColor(self.image_canvas,cv2.COLOR_BGR2GRAY)
        _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img,imgInv)
        img = cv2.bitwise_or(img,self.image_canvas)

        _,jpeg = cv2.imencode('.jpg',img)
        return jpeg.tobytes()



    



    




