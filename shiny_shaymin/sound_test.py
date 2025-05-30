import os

import librosa
import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd

main_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "main.wav")
clip_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "clip.wav")

fs = 48000
seconds = 30
channels = 1

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
    pass # should be a break

found = False
start_index = -1
for i in range(main_mfccs.shape[1] - clip_mfccs.shape[1] + 1):
    corr_matrix = np.corrcoef(main_mfccs[:, i:i + clip_mfccs.shape[1]], clip_mfccs)
    if corr_matrix[0, 1] == 1 and corr_matrix[1, 1] >= threshold and corr_matrix[2, 1] >= threshold and corr_matrix[3, 1] >= threshold and corr_matrix[4, 1] >= threshold and corr_matrix[5, 1] >= threshold and corr_matrix[6, 1] >= threshold and corr_matrix[7, 1] >= threshold and corr_matrix[8, 1] >= threshold and corr_matrix[9, 1] >= threshold and corr_matrix[10, 1] >= threshold and corr_matrix[11, 1] >= threshold:
        found = True

if found:
    print("found shiny")
else:
    print("no shiny")