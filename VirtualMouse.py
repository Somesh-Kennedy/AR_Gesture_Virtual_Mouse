# import the necessary libraries
import cv2
import numpy as np
import autopy
import HandTrackingModule as htm
import time
import pyautogui

 # set the camera resolution to 640x480
wCam, hCam = 640, 380
frameRed = 100 # frame reduction
count=1
screenshot_taken = False
smoothening = 7
plocx, plocy = 0, 0 # previous location of what coordinate
clocx, clocy = 0, 0 # current location of what coordinate

# initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0# Initialize the previous time variable for calculating FPS
detector = htm.handleDetector(maxHands=1)# maximum hand to be detected is set as 1
wScr, hScr = autopy.screen.size()
print(wScr, hScr)

# enter the loop that captures and displays the video feed
while True:
    # STEP 1 - Find hand landmarks

    success, img = cap.read()# read a frame from the camera. cap.read() returns two values.
    # a boolean value whether it reads it successfully or not and the image data
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)


    # STEP 2 -Get the tip of the index and the middle fingers

    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]#x1 and y1 are the points of the index finger
        x2, y2 = lmList[12][1:]#x2 and y2 are the points of the middle finger

        #print(x1,y1,x2,y2) # prints the coordinates of index and middle finger

    # STEP 3 -Check which fingers are up

        fingers = detector.fingersUp()
        print(fingers)
        cv2.rectangle(img, (frameRed, frameRed), (wCam - frameRed, hCam - frameRed), (255, 0, 255), 2)
    # STEP 4 -Only index finger : Moving mode

        if fingers[1]==1 and fingers[2]==0 and fingers[0]==0:#index is up and middle finger is down

    # STEP 5 -Convert coordinates i.e. the webcam which gives the result as 640x480 But the screen
    # resolution is 1536x864, so we need to convert the coordinates so that we get the correct positioning
            x3 = np.interp(x1, (frameRed, wCam - frameRed), (0, wScr))
            y3 = np.interp(y1, (frameRed, hCam - frameRed), (0, hScr))
    # STEP 6 -Smoothening the values

            clocx = plocx +(x3 - plocx) / smoothening
            clocy = plocy + (y3 - plocy) / smoothening
    # STEP 7 -Move the mouse        if fingers[0] == 1 and fingers[1] == 1 and fingers[2]==0:
            autopy.mouse.move(wScr - clocx,clocy)# wScr - x3 is done so that the mouse would move the same direction as the finger
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)#shows a circle when only index is shown
            plocx, plocy = clocx, clocy
    # STEP 8 -When both index and middle fingers
        # are up: clicking mode

        if fingers[1] == 1 and fingers[2] == 1:  # both index and middle finger is up
    # STEP 9 -find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            #print(length)
    # STEP 10 -Click mouse if the distance is short
            if length < 20:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 0, 255), cv2.FILLED)  # shows a circle when index and
                #middle finger touches
                autopy.mouse.click()
            # length = detector.findDistance(8, 12, img);
        if fingers[0] ==1 and fingers[1]==1 and fingers[2]==0 and fingers[4]==0:
            pyautogui.scroll(50)
        if fingers[0]==1 and fingers[1]==0 and fingers[2]==0:
            # length, img, lineInfo = detector.findDistance(8, 12, img)
            # if (length > 20):
            pyautogui.scroll(-50)
        if fingers[2]==1 and fingers[3]==1 and fingers[4]==1:
            length, img, lineInfo = detector.findDistance(4, 8, img)

            if length < 20 and screenshot_taken == False:
                # cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                screenshot_img = pyautogui.screenshot()
                screenshot_img.save('screenshot(' + str(count) + ').png')
                screenshot_taken = True  # to take only one screenshot at one time instead of a series
                count = count + 1
            elif length >= 20:
                screenshot_taken=False



    # STEP 11 -Frame rate
    cTime = time.time()# gets the current time in seconds
    fps = 1/(cTime-pTime)# calculates the FPS value
    pTime = cTime# sets the previous time (pTime) to the current time (cTime) for use in the next iteration of the loop.
    # cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)# adds the FPS value to the video frame
    # img: The image to write the text on
    # str(int(fps)): The text string to write, converted to an integer value of the FPS
    # (20,50): The position of the text on the image (x,y) coordinate
    # cv2.FONT_HERSHEY_PLAIN: The font type
    # 3: The font size
    # (255,0,0): The color of the text (in this case, blue)
    # 3: The thickness of the text stroke
    # STEP 12 -display
    cv2.imshow("Video Capture", img)# display the frame in a window called "Video Capture"
    cv2.waitKey(1)# wait for a key press event for 1 millisecond
