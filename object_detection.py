import cv2
import numpy as np
import builtins
import time
import imutils as im
import os
import math
from base_functions import altitude

cap = cv2.VideoCapture(0)
lower_hsv = np.array([75, 95, 130])
upper_hsv = np.array([180, 255, 255])
kernel = np.ones([3, 3], dtype=np.uint8)
listX = []
listY = []
x_distance = 0
y_distance = 0


def objectDetection():
    global x_distance, y_distance
    success, frame = cap.read()

    if not success:
        print("!!!!! Camera Connection is Failed !!!!!")

    if success:
        frameCopy = frame.copy()
        hsv = cv2.cvtColor(frameCopy, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

        open_ = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel)
        erode_ = cv2.erode(open_, kernel)
        dilate = cv2.dilate(erode_, kernel)

        contours, hier = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = builtins.max(contours, key=lambda x: cv2.contourArea(x), default=0)

        # ---------- Find Area ----------
        try:
            if len(c) > 150:
                rect = cv2.minAreaRect(c)
                rect_x, rect_y = rect[0]

                # ---- Center of Window
                h, w, c = frameCopy.shape
                h = int(h / 2)
                w = int(w / 2)

                # ----- Distance -----
                global x_distance, y_distance
                x_distance = np.int32(rect_x) - w
                y_distance = h - np.int32(rect_y)

                listX.append(x_distance)
                listY.append(y_distance)

                return "AREA-FOUND"
        except:
            pass


def pixels_per_meter_x(alt):
    return (alt * math.tan(math.radians(62.2 / 2))) / (640 / 2)


def pixels_per_meter_y(alt):
    return (alt * math.tan(math.radians(48.8 / 2))) / (480 / 2)
