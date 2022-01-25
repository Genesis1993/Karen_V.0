import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import speech_recognition as sr
import requests, sys, webbrowser, bs4
import urllib.request
import urllib.parse
import re

#Set AI Name
ai_name = "karen"


# Set voice parameter, Speed, volume and voice it self
engine = pyttsx3.init()
voices: object = engine.getProperty('voices')
# For loop just to see attribute of voices. note voices is dictionary, voice index is int
# i.name is str and i.languages is list
for i in voices:
    print(str(voices.index(i)) + ":" + i.name + ":" + i.languages[0])
engine.setProperty('voice', voices[33].id)  # Alex=0, Samantha =33, Victoria = 41
engine.setProperty('rate', 190)  # default rate is 200 meaning 200 words per minute
engine.setProperty('volume', 1)  # default is 1. min is 0 while max is 1

# Set z initial value as zero, caller to ai_name please see main while loop
z = 0

def say_text(text):
    engine.say(text)
    engine.runAndWait()


q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)


if args.model is None:
    args.model = '/Users/genesissales/PycharmProjects/Karen V.0/venv/lib/python3.8/site-packages/vosk/python/example/model'
if not os.path.exists(args.model):
    print ("Please download a model for your language from https://alphacephei.com/vosk/models")
    print ("and unpack as 'model' in the current folder.")
    parser.exit(0)
if args.samplerate is None:
    device_info = sd.query_devices(args.device, 'input')
    # soundfile expects an int, sounddevice provides a float:
    args.samplerate = int(device_info['default_samplerate'])

model = vosk.Model(args.model)

if args.filename:
    dump_fn = open(args.filename, "wb")
else:
    dump_fn = None

def readvoice():
    try:
        with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                                channels=1, callback=callback):
                print('#' * 80)
                print('Press Ctrl+C to stop the recording')
                print('#' * 80)

                rec = vosk.KaldiRecognizer(model, args.samplerate)
                while True:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                       #print(rec.Result)
                       y = rec.Result()
                       x = y[14:len(x)-3]
                       print(x)
                       print("listening...")
                    else:
                        x = ""
                    #     print(rec.PartialResult())
                    if 'play' in x:
                        song = x.replace('play', '')
                        say_text('playing ' + song)
                        pywhatkit.playonyt(song)
                    elif 'stop it' in x:
                        pywhatkit.close_tab()
                    elif 'who made you' in x:
                        say_text('I was created by my father, Genesis Ermitanyo Sales...He is '
                                 'an electrical engineer and a data scientist')
                    elif 'time' in x:
                        time = datetime.datetime.now().strftime('%I:%M %p')
                        say_text('Current time is ' + time)
                    elif 'who is' in x:
                        person = x.replace('who is', '')
                        info = wikipedia.summary(person, 1)
                        print(info)
                        say_text(info)
                    elif 'date' in x:
                        say_text('sorry, I have a headache')
                    elif 'are you single' in x:
                        say_text('I am in a relationship with wifi')
                    elif 'joke' in x:
                        say_text(pyjokes.get_joke())

                    elif 'thank you ' + ai_name in x:
                        say_text('Just call me anytime')
                    elif 'what is' in x:
                        word = x.replace('what is', '')
                        info = wikipedia.summary(word, 3)
                        print(info)
                        say_text(info)
                    if dump_fn is not None:
                        dump_fn.write(data)
    #Error Handling
    except KeyboardInterrupt:
        print('\nDone')
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))
    return x

while True:
    x = readvoice()

