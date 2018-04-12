#!/usr/bin/python2.7

from pyaudio import *
from pocketsphinx import *
from moviepy.editor import *
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import ffmpy as ffmpy
#from SpeechRecognition import *
import Tkinter # Python GUI package
import tkFileDialog # for Dialog Box
import traceback # for error checking
import tkMessageBox
import subprocess
import os, sys, datetime, time
from datetime import datetime

gui = Tkinter.Tk()
gui.attributes("-topmost")
gui.withdraw()
initialdir = "/home/alex/audio_recognition/videos/"
submit_time = datetime.now().strftime("%Y%m%d_%H%M")

ftypes = [
    ('All files', '*'),
    ('Python code files', '*.py'), 
    ('Perl code files', '*.pl;*.pm'),  # semicolon trick
    ('Java code files', '*.java'), 
    ('C++ code files', '*.cpp;*.h'),   # semicolon trick
    ('Text files', '*.txt') 
]

source_file = tkFileDialog.askopenfilename(parent=gui, initialdir=initialdir, title= 'Select a file to be analyzed', filetypes=ftypes)

def split_audio(filename, filepath):
    sound_file = AudioSegment.from_wav(filename)
    print(len(sound_file))
    iterations = len(sound_file)/3000
    left_over = len(sound_file)-(iterations*3000)
    print str(iterations)
    print str(left_over)
    iteration = 1
    chunks = []
    #audio_chunks = split_on_silence(sound_file, min_silence_len=10, silence_thresh=100)
    #print(str(audio_chunks))
    #for i, chunk in enumerate(audio_chunks):
    #    print(str(i, chunk))
    #    out_file = "audio_learning/audios/" + filename + "_splitAudio/" + filename + "_chunk{0}.wav".format(i)
    #    print("exporting", out_file)
    #    chunk.export(out_file, format="wav") 
    while iteration <= iterations:
        clip = sound_file[iteration*3000:(iteration*3000)+3000]
        out_file = filepath + "/" + filename_base + "_chunk" + str(iteration) + ".wav"
        print("exporting", out_file)
        clip.export(out_file, format="wav")
        iteration = iteration + 1
        chunks.append(str(out_file))
    last_clip = sound_file[-left_over:]
    out_file_last = filepath + "/" + filename_base + "_chunk" + str(iterations + 1) + ".wav"
    chunks.append(str(out_file_last))
    print ("exporting", out_file_last)
    last_clip.export(out_file_last, format="wav")
    return (chunks)

def convert(filename_base, filepath):
    command1 = str("ffmpeg -i " + str(source_file) + " -vn " + str(filename))
    subprocess.check_output(command1, shell=True)
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    # Once converted to .wav format we can now use for speech recognition

def sphinx_recognize(source_file):
    r = sr.Recognizer()
    with sr.AudioFile(source_file) as source:
        framerate = 100
        audio = r.record(source) # read the entire audio file
        decoder = r.recognize_sphinx(audio, show_all=False)
    try:
        #print([(seg.word, seg.start_frame/framerate)for seg in decoder])
        print("Sphinx thinks you said:  \n\n")
        print('"' + decoder + '"')
        print("\n\n")
        #print(decoder.seg())
        print("\n\n")
        
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

def google_recognize(source_file):
    r = sr.Recognizer()
    with sr.AudioFile(source_file) as source:
        audio = r.record(source) # read the entire audio file
    try:    
        print("Google thinks you said:  \n\n")
        print('"' + r.recognize_google(audio) + '"')
        print("\n\n")
    except sr.UnknownValueError:
        print("Google could not understand audio")
    except sr.RequestError as e:
        print("Could not complete request for Google Speech Recognition service; {0}".format(e))
        
        
        
        
def write_caption(video, captions):
    for clip in captions:
        video = VideoFileClip(str(video)).subclip(clip[0], clip[1])
        txt_clip = (TextClip(str(clip[3]), fontsize=18,color='white').set_position('center').set_duration(clip[1]-clip[0])) 
        
        
        
        
print(str(source_file))


init_filename_list = source_file.split('/')
init_filename = init_filename_list[-1]
filename_base_list = init_filename.split('.')
filename_base = filename_base_list[0] + "_" + submit_time
filename = str("audios/" + str(filename_base) + ".wav")
filepath = str("audios/" + str(filename_base) + "_split_audio")


if source_file.endswith('.wav'):
    clips = split_audio(filename_base, filepath)
    print clips
    print("\n\nSphinx is now analyzing the audio for speech recognition\n\n")
    for clip in clips:
        print clip
        sphinx_recognize(clip)
else:
    convert(filename_base, filepath)
    clips = split_audio(filename, filepath)
    print clips
    print("\n\nSphinx is now analyzing the audio for speech recognition\n\n")
    for clip in clips:
        print clip
        sphinx_recognize(clip)
