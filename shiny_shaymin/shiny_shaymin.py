import os
import time

import librosa
import numpy as np
from scipy.io.wavfile import write
import serial
import sounddevice as sd

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

main_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "main.wav")
clip_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "clip.wav")

fs = 48000
seconds = 20
channels = 1

ser = serial.Serial("COM3", 115200)
ser.write(bytearray("+IMM 000002 \n", "ascii"))
time.sleep(2)

count = 0

while True:
    # AED failed: no shiny

    ser.write(bytearray("+IMM 000004 \n", "ascii"))
    time.sleep(2)

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

    print("Recording...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=channels)
    sd.wait()  # Wait until recording is finished
    print("Recording complete")

    write(main_filepath, fs, myrecording)
    print(f"Saved as {main_filepath}")

    main_data, _ = librosa.load(main_filepath, sr=fs)
    clip_data, _ = librosa.load(clip_filepath, sr=fs)

    threshold = 0.99999999

    main_mfccs = librosa.feature.mfcc(y=main_data, sr=fs)
    clip_mfccs = librosa.feature.mfcc(y=clip_data, sr=fs)

    if clip_mfccs.shape[1] > main_mfccs.shape[1]:
        break

    found = False
    start_index = -1
    for i in range(main_mfccs.shape[1] - clip_mfccs.shape[1] + 1):
        corr_matrix = np.corrcoef(main_mfccs[:, i:i + clip_mfccs.shape[1]], clip_mfccs)
        if corr_matrix[0, 1] == 1 and corr_matrix[1, 1] >= threshold and corr_matrix[2, 1] >= threshold and corr_matrix[3, 1] >= threshold and corr_matrix[4, 1] >= threshold and corr_matrix[5, 1] >= threshold and corr_matrix[6, 1] >= threshold and corr_matrix[7, 1] >= threshold and corr_matrix[8, 1] >= threshold and corr_matrix[9, 1] >= threshold and corr_matrix[10, 1] >= threshold and corr_matrix[11, 1] >= threshold:
            found = True

    if found:
        print("found shiny")
        break
    else:
        print("no shiny")

    count = count + 1
    print(f"attempt: {count}")
