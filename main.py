import cv2
import numpy as np
import HandTrackingModule as htm
import autopy
import time

###########################
widthcam,heightcam=640,480
frameR=100 #frame reduction
widthscr,heightscr=autopy.screen.size()
detector=htm.handDetector(maxHands=1)

smooth=5
plocx,plocy=0,0
currlocx,currlocy=0,0
##########################
cap=cv2.VideoCapture(0)

cap.set(3,widthcam)
cap.set(4,heightcam)
pTime=0

while True:
    success, img=cap.read()


    img=detector.findHands(img)
    lmList,bbox=detector.findPosition(img)
    #########################
    if(len(lmList)!=0):
        x1,y1 = lmList[8][1:]#index finger
        x2,y2 = lmList[12][1:]#middle finger

    #############
    fingers= detector.fingersUp()
    ################################

    ## check is index finger  up
    try:
        if fingers[1]==1 and fingers[2]==0:
            cv2.rectangle(img,(frameR,frameR),(widthcam-frameR,heightcam-frameR),(255,0,255),2)
            x3 = np.interp(x1,(frameR,widthcam-frameR),(0,widthscr))
            y3 = np.interp(y1,(frameR,widthcam-frameR),(0,widthscr))
            currlocx=plocx+(x3-plocx)/smooth
            currlocy=plocy+(y3-plocy)/smooth

            autopy.mouse.move(widthscr-currlocx,currlocy)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocx,plocy=currlocx,currlocy

        if fingers[1]==1 and fingers[2]==1 and fingers[0]==0 and fingers[3]==0 and fingers[4]==0:
            length,img,lineinfo=detector.findDistance(8,12,img)
            print(length)
            if length<25:
                cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
                print("douple click")


    except:
        print("no hand detected")


    ####################

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    #####################
    cv2.imshow("image",img)
    cv2.waitKey(1)

