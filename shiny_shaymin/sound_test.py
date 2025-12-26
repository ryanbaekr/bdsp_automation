import math

import numpy as np
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
INDEX = 2
RECORD_SECONDS = 15

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

print(score)
