from vosk import Model, KaldiRecognizer
import pyaudio


model = Model('/Users/genesissales/PycharmProjects/Karen V.0/venv/lib/python3.8/site-packages/vosk/python/example/model')
recognizer = KaldiRecognizer(model, 1600)

# Recognize from the microphone

cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=1600, input=True, frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4096)

    if recognizer.AcceptWaveform(data):
        print(recognizer.Result())