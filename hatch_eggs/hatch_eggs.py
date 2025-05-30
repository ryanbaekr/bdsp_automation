import time

import serial

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

ser = serial.Serial("COM3", 115200)
ser.write(bytearray("+IMM 000008 \n", "ascii"))
time.sleep(2)

boxes = 17  # number of full boxes of eggs
rights = 1

for box in range(boxes * 6):
    for i in range(22):
        ser.write(bytearray("+IMM 000000 \n", "ascii"))
        time.sleep(11.5)
        ser.write(bytearray("+IMM 000004 \n", "ascii"))
        time.sleep(11.5)

    for i in range(5):
        for j in range(5):
            ser.write(bytearray("+IMM 000208 \n", "ascii"))
            time.sleep(0.5)
            ser.write(bytearray("+IMM 000008 \n", "ascii"))
            time.sleep(5.5)

    # open menu
    ser.write(bytearray("+IMM 000808 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.5)

    # open party
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.5)

    # open box
    ser.write(bytearray("+IMM 002008 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.5)

    # quick sort
    ser.write(bytearray("+IMM 000108 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.5)

    # left
    ser.write(bytearray("+IMM 000006 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.5)

    # up
    ser.write(bytearray("+IMM 000000 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.5)

    for i in range(5):
        # down twice
        for j in range(2):
            ser.write(bytearray("+IMM 000004 \n", "ascii"))
            time.sleep(0.5)
            ser.write(bytearray("+IMM 000008 \n", "ascii"))
            time.sleep(0.5)

        # pick up phione
        ser.write(bytearray("+IMM 000408 \n", "ascii"))
        time.sleep(0.5)
        ser.write(bytearray("+IMM 000008 \n", "ascii"))
        time.sleep(0.5)

        # up
        ser.write(bytearray("+IMM 000000 \n", "ascii"))
        time.sleep(0.5)
        ser.write(bytearray("+IMM 000008 \n", "ascii"))
        time.sleep(0.5)

        for j in range(rights):
            ser.write(bytearray("+IMM 000002 \n", "ascii"))
            time.sleep(0.5)
            ser.write(bytearray("+IMM 000008 \n", "ascii"))
            time.sleep(0.5)

        # swap egg
        ser.write(bytearray("+IMM 000408 \n", "ascii"))
        time.sleep(0.5)
        ser.write(bytearray("+IMM 000008 \n", "ascii"))
        time.sleep(0.5)

        for j in range(rights):
            ser.write(bytearray("+IMM 000006 \n", "ascii"))
            time.sleep(0.5)
            ser.write(bytearray("+IMM 000008 \n", "ascii"))
            time.sleep(0.5)

    rights = rights + 1
    if rights >= 7:
        rights = 1

        # next box
        ser.write(bytearray("+IMM 002008 \n", "ascii"))
        time.sleep(0.5)
        ser.write(bytearray("+IMM 000008 \n", "ascii"))
        time.sleep(0.5)

    # close box
    ser.write(bytearray("+IMM 000208 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.5)

    # close party
    ser.write(bytearray("+IMM 000208 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.5)

    # close menu
    ser.write(bytearray("+IMM 000208 \n", "ascii"))
    time.sleep(0.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.5)
