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
    ||||||_ -
    |||||__ +
    ||||___ LS
    |||____ RS
    ||_____ HOME
    |______ CAPTURE

Byte 1
0b00000000
  ||||||||_ Y
  |||||||__ B
  ||||||___ A
  |||||____ X
  ||||_____ L
  |||______ R
  ||_______ ZL
  |________ ZR

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
RECORD_SECONDS = 20  # may need to be increased for switch 1
THRESHOLD = 275000  # typical non-shiny is 270000, shiny was 340000

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
  - ~270000
- shiny:
  - ~340000
"""

count = 0

while True:
    # start game
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(11.55)

    # skip title sequence
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(2.25 + random.randint(0, 3)/60)

    # press start
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(6.25 + random.randint(0, 3)/60)

    # talk to heatran
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.45)

    # start battle
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.45)

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

    # close game
    # home
    ser.write(bytearray("+IMM 100008 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.85)
    # x
    ser.write(bytearray("+IMM 000808 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.35)
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(0.85)
