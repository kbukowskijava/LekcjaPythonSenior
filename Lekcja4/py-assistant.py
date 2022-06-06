import speech_recognition as sr
import gtts
import webbrowser
import urllib
import os
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import pygame

pygame.init()

speak_engine = pyttsx3.init()
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[1].id)

path = os.path.dirname(os.path.abspath(__file__))

# commands
opts = {
    'name': ('lillian', 'lilly', 'li', 'lili', 'lily'),
    'user_command': ('tell', 'say', 'show', 'how many', 'how', 'search'),
    'cmds': {
        'ctime': ('time', 'what time', 'the time'),
        'paint': ('paint', 'draw', 'art'),
        'google': ('find', 'google search', 'google'),
        'youtube': ('video', 'youtube', 'music')
    }
}


# Write voice
def command():
    r = sr.Recognizer()

    with sr.Microphone(device_index=1) as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language='en-EN').lower()
        # text = r.recognize_google(audio, language='fr-FR').lower()
        print('[log] Recognized: ' + text)

    except sr.UnknownValueError:
        print('[log] Voice not recognized!')
    except sr.RequestError as e:
        print('[log] Unknown error, check the internet!')
    except:
        text = command()
    return text


# Convert text to speech
# method 1
def text_to_speech(text):
    tts = gtts.gTTS(text)
    speech_path = os.path.join((path + '/speech.mp4'))
    tts.save(speech_path)
    pygame.mixer.music.load('speech.mp4')
    pygame.mixer.music.play()


# Convert text to speech
# method 2
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(text):
    if text.startswith(opts['name']):
        cmd = text

        for x in opts['name']:
            cmd = cmd.replace(x, "").strip()

        for x in opts['user_command']:
            cmd = cmd.replace(x, "").strip()

        cmd = recognize_cmd(cmd)
        execute_cmd(cmd['cmd'])


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak('Time  ' + str(now.hour) + ':' + str(now.minute))

    elif cmd == 'paint':
        os.system("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Paint")

    elif cmd == 'google':
        cmd = cmd.replace('google', "").strip()
        speak('The Google content has been opened for you')
        google_search(cmd)

    elif cmd == 'youtube':
        cmd = cmd.replace('youtube', "").strip()
        speak('The Youtube has been opened for you')
        youtube_search(cmd)

    else:
        print('Not recognized! Repeat, please!')


def google_search(text):
    tes = urllib.parse.quote_plus(text)
    url = 'https://www.google.com/search?q='
    webbrowser.open(url + tes, new=2)


def youtube_search(text):
    tes = urllib.parse.quote_plus(text)
    url = 'https://www.youtube.com/results?search_query='
    webbrowser.open(url + tes, new=2)


if __name__ == '__main__':
    execute_cmd(command())
