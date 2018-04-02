#!/usr/bin/python2.7

from pyaudio import *
from pocketsphinx import *
import speech_recognition as sr
#from SpeechRecognition import *
import Tkinter # Python GUI package
import tkFileDialog # for Dialog Box
import traceback # for error checking
import tkMessageBox
import os, sys, datetime, time
from datetime import datetime

gui = Tkinter.Tk()
gui.attributes("-topmost")
gui.withdraw()
initialdir = "/home/alex/audio_recognition/videos"

ftypes = [
    ('Python code files', '*.py'), 
    ('Perl code files', '*.pl;*.pm'),  # semicolon trick
    ('Java code files', '*.java'), 
    ('C++ code files', '*.cpp;*.h'),   # semicolon trick
    ('Text files', '*.txt'), 
    ('All files', '*'), 
]

source_audio_file = tkFileDialog.askopenfilename(parent=gui, initialdir=initialdir, title= 'Select an audio file to be analyzed', filetypes=ftypes)

# use the source_audio_file as the audio source
r = sr.Recognizer()
with sr.AudioFile(source_audio_file) as source:
    audio = r.record(source) # read the entire audio file

print(str(source_audio_file))

try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))
