import os
import time

import cv2

cap = cv2.VideoCapture(1)  # default: 0

if not cap.isOpened():
    raise IOError("Cannot open webcam")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

"""
ret, frame = cap.read()

if ret:
    cv2.imwrite("baseline.png", frame)

    cap.release()
    cv2.destroyAllWindows()
"""

template_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "baseline.png")
template = cv2.imread(template_filepath)

method = cv2.TM_SQDIFF_NORMED

"""
trim
from left:   190
from right:  1600
from top:    660
from bottom: 360
"""

while True:
    ret, frame = cap.read()

    if not ret:
        break

    result = cv2.matchTemplate(frame, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(min_val)
    print(min_loc)

    time.sleep(0.5)

cap.release()
cv2.destroyAllWindows()
