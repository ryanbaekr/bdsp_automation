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
RECORD_SECONDS = 22  # may need to be increased for switch 1
THRESHOLD = 340000  # typical non-shiny is 320000, shiny was 390000

ser = serial.Serial("COM3", 115200)
ser.write(bytearray("+IMM 000002 \n", "ascii"))
time.sleep(.3)
ser.write(bytearray("+IMM 000008 \n", "ascii"))
time.sleep(.3)
ser.write(bytearray("+IMM 000002 \n", "ascii"))
time.sleep(.3)
ser.write(bytearray("+IMM 000008 \n", "ascii"))
time.sleep(.3)
ser.write(bytearray("+IMM 100008 \n", "ascii"))
time.sleep(.3)
ser.write(bytearray("+IMM 000008 \n", "ascii"))
time.sleep(.3)

time.sleep(1)

count = 0

while True:
    # up to run button
    ser.write(bytearray("+IMM 000000 \n", "ascii"))
    time.sleep(.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(.5)

    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(.5)
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(.5)

    # tap b through text
    for i in range(5):
        ser.write(bytearray("+IMM 000208 \n", "ascii"))
        time.sleep(.5)
        ser.write(bytearray("+IMM 000008 \n", "ascii"))
        time.sleep(.5)

    ser.write(bytearray("+IMM 000204 \n", "ascii"))
    time.sleep(3.3)

    ser.write(bytearray("+IMM 000200 \n", "ascii"))
    time.sleep(3.7)

    # tap a through text
    for i in range(5):
        ser.write(bytearray("+IMM 000408 \n", "ascii"))
        time.sleep(.5)
        ser.write(bytearray("+IMM 000008 \n", "ascii"))
        time.sleep(.5)

    # wait for battle to start
    time.sleep(.7)

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
