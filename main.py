import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import speech_recognition as sr
#  import requests, sys, webbrowser, bs4
import urllib.request
import urllib.parse
import re
import time

ai_name = "tony"  # setting AI name

#  Setting which microphone to use
mic_list = sr.Microphone.list_microphone_names()  # will get the list of all microphone connected
print(mic_list)
device_index = mic_list.index('MacBook Air Microphone')  #
mic = sr.Microphone(device_index=device_index)

# shorthand sr.Recognizer() as recog for easy typing
recog = sr.Recognizer()

# Set voice parameter, Speed, volume and voice it self
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# For loop just to see attribute of voices. note voices is dictionary, voice index is int
# i.name is str and i.languages is list


for i in voices:
    print(str(voices.index(i)) + ":" + i.name + ":" + i.languages[0])
engine.setProperty('voice', voices[33].id)  # Alex=0, Samantha =33, Victoria = 41
engine.setProperty('rate', 190)  # default rate is 200 meaning 200 words per minute
engine.setProperty('volume', .1)  # default is 1. min is 0 while max is 1

# Set z initial value as zero, caller to ai_name please see main while loop
z = 0


def write_voice():
    with mic:  # with is the manifistation or shorthand of mic._enter_ and _exit_
        print("I'm listening")
        recog.adjust_for_ambient_noise(mic, duration=.5)  # listener.adjust_for_ambient_noise(mic,#duration=5)
        # audio_stopper = recog.listen_in_background(mic, callback)  #callback as a link will call the function dont
        # use parentesis because it gives results just the name of the function for th mother function to use it as his
        voice = recog.listen(mic)  # set voice as the signal created from the .listen function of SR

    try:
        ctext = recog.recognize_google(voice)  # Cotext as converted text from voice using SR
        ctext = ctext.lower()
        print(ctext)

    except sr.RequestError:
        print("Request error might be cause of poor internet")
        ctext = ""

    except sr.UnknownValueError:
        print("Can't recognize you are saying")
        ctext = ""

    except sr.WaitTimeoutError:
        print("wait time error")
        ctext = ""

    return ctext


print(mic.list_microphone_names()[device_index])


# def callback(recog, audio):
#     print(recog.recognize_google(audio))


def say_text(text: str):
    engine.say(text)
    engine.runAndWait()


def parsing(url):
    values = {'s': 'basics',
              'submit': 'search'}
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    resp = urllib.request.urlopen(req)
    resp_data = resp.read()
    paragraphs = re.findall(r'<p>(.*?)</p>', str(resp_data))
    print(paragraphs)
    # for eachP in paragraphs:
    #     print(eachP)

    return paragraphs


def command(x: str):
    try:
        # if x == 'tony':
        #     say_text('Yes Sir?')
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
            timed = datetime.datetime.now().strftime('%I:%M %p')
            say_text('Current time is ' + timed)
        elif 'who is' in x:
            person = x.replace('who is', '')
            info = wikipedia.summary(person, 1)
            print(info)
            say_text(info)
        elif 'date' in x:
            say_text('sorry i have an headache')
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
        elif 'spell' in x:
            x = x.replace('spell', "")
            x = x.replace(' ', '')
            y = list(x)
            for letter in y:
                engine.setProperty('volume', 1)
                time.sleep(1)
                say_text(letter)
                time.sleep(1)
            engine.setProperty('volume', .2)
    except wikipedia.exceptions.PageError:  # handling specific error by the use of try and except
        say_text("I can't see it on wikipedia... You want me to search it on youtube?")
    except NameError:
        say_text("I do not know him name error")
        # elif 'google' in x:
        #     word = x.replace('google', '')
        #     info = gs.search(word)
        #     info = info[1]
        #     print(info)
        #     n = parsing(info)
        #     say_text(n)

        # else:
        #     print('Please say the command again.')


while True:
    # say_text("Now, instead of using an audio file as the source, you will use the default system microphone.
    # You can access this by creating an instance of the Microphone class.")
    a = write_voice()
    if a == ai_name:
        z = 1
        say_text("yes sir?")

    while z == 1:
        a = write_voice()
        if a == 'thank you ' + ai_name:
            z = 0
        command(a)
        print(z)
    # spell = speech.speech("easy")
    # print(Spell)
