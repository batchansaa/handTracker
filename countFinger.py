"""
Author: Batchansaa Batzorig
Date: October 2021

Count how many fingers there are through OpenCV.
"""

import cv2
import os
import HandTrackingModule as htm
from tkinter import Tcl


def setUp():
    folderPath = "numberImages"
    myList = os.listdir(folderPath)
    myList = Tcl().call('lsort', '-dict', myList)

    overlayList = []

    for imagePath in myList:
        image = cv2.imread(f'{folderPath}/{imagePath}')
        overlayList.append(image)
    return overlayList


def main():
    cameraWidth = 640
    cameraHeight = 480

    cap = cv2.VideoCapture(0)
    cap.set(3, cameraWidth)
    cap.set(4, cameraHeight)

    overlayList = setUp()

    detector = htm.handDetector(detectionCon=0.75)
    # ids for different fingers (thumb to pinky)
    tipIds = [4, 8, 12, 16, 20]
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPositions(img, draw=False)

        if len(lmList) != 0:
            fingers = []
            # for left hand
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(0)
            else:
                fingers.append(1)

            # 4 fingers
            for index in range(1, 5):
                if lmList[tipIds[index]][2] < lmList[tipIds[index] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)
            h, w, c = overlayList[totalFingers - 1].shape
            img[0:h, 0:w] = overlayList[totalFingers - 1]

        cv2.imshow("How many fingers?", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
