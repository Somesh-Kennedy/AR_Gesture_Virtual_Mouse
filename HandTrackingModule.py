import cv2  # module used for video and photo analysis
import mediapipe as mp
import time # to calculate the fps
import math

class handleDetector():
    def __init__(self, mode=False, maxHands = 2, model_complexity= 1,detectionConfidence = 0.5, trackConfidence = 0.5): #initialization part
        self.results = None
        self.mode = mode
        self.model_complexity = model_complexity
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.trackConfidence = trackConfidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity, self.detectionConfidence, self.trackConfidence) # The Hands() object from mpHands is then used to detect and track hands in the RGB image.
        self.mpdraw = mp.solutions.drawing_utils

    def findHands(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #It converts each frame from the default BGR format to RGB format using cv2.cvtColor(), which is required for the mpHands.Hands() object to process the image.
        self.results = self.hands.process(imageRGB) #contains information about the detected hand landmarks #set results with self so that you can use it any function.
        # print(results.multi_hand_landmarks) #to see something is detected or not

        if self.results.multi_hand_landmarks:
            for handsLmarks in self.results.multi_hand_landmarks: #will give the id number and the landmarks information which contains x, y and z co-ordinates values
               if draw:
                   self.mpdraw.draw_landmarks(image, handsLmarks, self.mpHands.HAND_CONNECTIONS)
        return image

    def findPosition(self, image, hand_number=0, draw = True ): #to find the position of the particular hand
        xList = []
        yList = []
        bbox = []
        self.lmList = [] #to store the positions of the hands in list
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_number] #we are getting only the landmarks of the particular hand or the landmarks of the hand_number-th hand are extracted from self.results.multi_hand_landmarks and the lmList variable is initialized to an empty list.
            for id, lm in enumerate(hand.landmark):  # Enumerate() method adds a counter to an iterable and returns it in a form of enumerating object.
                height, width, channels = image.shape  # give the height and width of the image
                cx, cy = int(lm.x * width), int(lm.y * height)  # The landmark coordinates are then converted to pixel values using the image height and width, and the resulting (x, y) values are stored in the cx and cy variables.
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy]) #append the values of id, cx, cy to the list
                # print(self.lmList)
                if draw:
                    cv2.circle(image, (cx, cy), 10, (0, 255, 0),cv2.FILLED)  # use to draw circle for the given index using the pixels

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(image, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)

        return self.lmList, bbox

    def fingersUp(self):
        fingers = []
        self.tipIds = [4, 8, 12, 16, 20]
        #thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #Fingers
        for i in range(1, 5):

            if self.lmList[self.tipIds[i]][2] < self.lmList[self.tipIds[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        #totalFingers = fingers.count(1)
        return fingers


    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # if draw:
            # cv2.line(img, (x1,y1), (x2,y2), (255,0,255),t)
            # cv2.circle(img, (x1,y1), r,(255,0,255), cv2.FILLED)
            # cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            # cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1) #finding the euclidian distance

        return length, img, [x1, y1, x2, y2, cx, cy]




def main():

    prev_time = 0
    curr_time = 0
    cap = cv2.VideoCapture(0)  # get a video capture object for the camera. 0 - webcam 1 - external cameras
    detector = handleDetector()

    while True:
        status, image = cap.read()  # read frames from the video and store it in the img and set the booleam value to the variable status
        image = detector.findHands(image)
        lmList, bbox = detector.findPosition(image)
        # if len(lmList) != 0:
        #     print(lmList[4]) #print the values with index 4 i.e id no. 4 or 4th point in the hand landmark
        curr_time = time.time()  # getting the current time using time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 4)  # to display fps (image, displaying fps as string, location, font style, scale, color, thickness)

        cv2.imshow("Video Capture", image)
        cv2.waitKey(1)  # the program will only wait for 1 millisecond for a key press before continuing to the next iteration of the loop


if __name__ == "__main__":
    main()