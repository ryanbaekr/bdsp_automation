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

count = 0

while count < 600:  # roughly 1.1 * the number of eggs desired
    for i in range(37):
        ser.write(bytearray("+IMM 000206 \n", "ascii"))
        time.sleep(.5)
        ser.write(bytearray("+IMM 000202 \n", "ascii"))
        time.sleep(.5)

    for i in range(8):
        ser.write(bytearray("+IMM 000408 \n", "ascii"))
        time.sleep(.5)
        ser.write(bytearray("+IMM 000008 \n", "ascii"))
        time.sleep(1.5)

    for i in range(4):
        ser.write(bytearray("+IMM 000208 \n", "ascii"))
        time.sleep(.5)
        ser.write(bytearray("+IMM 000008 \n", "ascii"))
        time.sleep(1)

    count = count + 1
    print(count)
