import random
import time
import math

import numpy as np
import pyaudio
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

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
INDEX = 2
RECORD_SECONDS = 12  # may need to be increased for switch 1
THRESHOLD = 370000  # typical non-shiny is 360000, shiny was 430000

ser = serial.Serial("COM3", 115200)

# get the controller connected
for i in range(0, 3):
    # zr
    ser.write(bytearray("+IMM 008008 \n", "ascii"))
    time.sleep(0.3)
    # zl
    ser.write(bytearray("+IMM 004008 \n", "ascii"))
    time.sleep(0.3)

"""
expectations:
- not shiny:
  - ~360000
- shiny:
  - ~430000
"""

count = 5906

while True:
    # open menu
    # x
    ser.write(bytearray("+IMM 000808 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.5)

    # select 'pokemon'
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.5)

    # select the first pokemon in your party
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.3)

    # navigate to 'sweet scent'
    # down
    ser.write(bytearray("+IMM 000004 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.3)

    # select 'sweet scent'
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(2.0)

    print("started recording")

    p = pyaudio.PyAudio()
    print(p.get_device_info_by_index(INDEX))
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=INDEX,
    )

    frames = []

    for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        samples = np.frombuffer(data, dtype=np.int16)
        frames.append(samples)

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = np.concatenate(frames)

    score = sum(math.sqrt(abs(sample))//10 for sample in audio_data)
    print(f"score: {score}")

    if score > THRESHOLD:
        print("found shiny")
        break
    else:
        print("no shiny")

    count = count + 1
    print(f"attempt: {count}")

    # navigate to 'run'
    # up
    ser.write(bytearray("+IMM 000000 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.3)

    # select 'run'
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(4.0 + random.randint(0, 30)/120)
