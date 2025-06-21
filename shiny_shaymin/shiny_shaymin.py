import os
import time

import serial
import cv2

"""
https://github.com/knflrpn/SwiCC_RP2040

Byte 0
0b00000000
    |||||\_ -
    ||||\__ +
    |||\___ LS
    ||\____ RS
    |\_____ HOME
    \______ CAPTURE

Byte 1
0b00000000
  |||||||\_ Y
  ||||||\__ B
  |||||\___ A
  ||||\____ X
  |||\_____ L
  ||\______ R
  |\_______ ZL
  \________ ZR

Byte 2
0x00 - Up
0x01 - Up/Right
0x02 - Right
0x03 - Down/Right
0x04 - Down
0x05 - Down/Left
0x06 - Left
0x07 - Up/Left
0x08 - Neutral
"""

template_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "baseline.png")
template = cv2.imread(template_filepath)

method = cv2.TM_SQDIFF_NORMED

ser = serial.Serial("COM3", 115200)
ser.write(bytearray("+IMM 000002 \n", "ascii"))
time.sleep(0.5)
ser.write(bytearray("+IMM 000008 \n", "ascii"))
time.sleep(0.5)
ser.write(bytearray("+IMM 000002 \n", "ascii"))
time.sleep(0.5)
ser.write(bytearray("+IMM 000008 \n", "ascii"))
time.sleep(0.5)
ser.write(bytearray("+IMM 100008 \n", "ascii"))
time.sleep(0.3)
ser.write(bytearray("+IMM 000008 \n", "ascii"))
time.sleep(1.5)

"""
expectations:
- shiny:
  - 0.000000 < val < 0.000002
  - 190, 660
- not shiny:
  - 0.030086 < val < 0.030087
  - 163, 660
"""

count = 6100

while True:
    # start game
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.5)

    # skip update
    ser.write(bytearray("+IMM 000000 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.5)

    # wait for user select
    time.sleep(2)

    # select user
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.5)

    # wait for game to open
    time.sleep(30)

    # a to start
    for i in range(4):
        ser.write(bytearray("+IMM 000408 \n", "ascii"))
        time.sleep(.5)
        ser.write(bytearray("+IMM 000008 \n", "ascii"))
        time.sleep(.5)

    # wait for save to load
    time.sleep(18)

    # start battle
    for i in range(5):
        ser.write(bytearray("+IMM 000408 \n", "ascii"))
        time.sleep(.5)
        ser.write(bytearray("+IMM 000008 \n", "ascii"))
        time.sleep(.5)

    # wait for battle to start
    time.sleep(24)

    # catch
    ser.write(bytearray("+IMM 000808 \n", "ascii"))
    time.sleep(0.3)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.3)
    ser.write(bytearray("+IMM 000002 \n", "ascii"))
    time.sleep(0.3)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.3)
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.3)

    # wait for catch animation
    time.sleep(20)

    # tap b through text
    for i in range(5):
        ser.write(bytearray("+IMM 000208 \n", "ascii"))
        time.sleep(.5)
        ser.write(bytearray("+IMM 000008 \n", "ascii"))
        time.sleep(.5)

    # wait for catch screen to close
    time.sleep(5)

    # check party
    ser.write(bytearray("+IMM 000808 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.5)
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.5)
    ser.write(bytearray("+IMM 000004 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.5)
    for i in range(2):
        ser.write(bytearray("+IMM 000408 \n", "ascii"))
        time.sleep(.5)
        ser.write(bytearray("+IMM 000008 \n", "ascii"))
        time.sleep(1.5)

    cap = cv2.VideoCapture(1)  # default: 0

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    ret, frame = cap.read()

    if not ret:
        break

    result = cv2.matchTemplate(frame, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    cap.release()
    cv2.destroyAllWindows()

    print(min_val)
    print(min_loc)

    if min_val < 0.03 or min_loc[0] > 165:
        break

    count = count + 1
    print(count)

    # close game
    ser.write(bytearray("+IMM 100008 \n", "ascii"))
    time.sleep(0.3)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.5)
    ser.write(bytearray("+IMM 000808 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.5)
