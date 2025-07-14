import cv2
import pyautogui
import sys
import os
import time

# Add hand-tracking folder to Python path
sys.path.append(os.path.abspath('../hand-tracking'))
from cvzone.HandTrackingModule import HandDetector

class VirtualMouse:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(maxHands=1, detectionCon=0.7, modelComplexity=0, minTrackCon=0.7)
        self.screen_width, self.screen_height = pyautogui.size()
        self.index_coords = None
        self.prev_index_x = 0
        self.fist_flag = False  # 👊 Closed fist detection
        self.gun_flag = False   # 🤠 Gun gesture detection

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue
            hands, frame = self.detector.findHands(frame, draw=False)

            if hands:
                hand = hands[0]  # First detected hand
                hand_type = hand['type']  # 'Left' or 'Right'
                print(f"Detected hand: {hand_type}")

                lmList = hand['lmList']

                # Scale index finger tip to screen size
                frame_h, frame_w = self.cap.get(4), self.cap.get(3)
                index_x = int((lmList[8][0] / frame_w) * self.screen_width)
                index_y = int((lmList[8][1] / frame_h) * self.screen_height)
                self.index_coords = (index_x, index_y)

                # Check if all fingers are down (fist)
                fingers = self.detector.fingersUp(hand)
                self.fist_flag = (sum(fingers) == 0)
                # Gun gesture: thumb and index up, others down
                self.gun_flag = (fingers == [1, 1, 0, 0, 0])
            else:
                self.fist_flag = False
                self.gun_flag = False
