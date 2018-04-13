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
    ('All files', '*')
]

source_file = tkFileDialog.askopenfilename(parent=gui, initialdir=initialdir, title= 'Select a file to be analyzed', filetypes=ftypes)
init_filename_list = source_file.split('/')
init_filename = init_filename_list[-1]
filename_base_list = init_filename.split('.')
filename_base = filename_base_list[0] + "_" + submit_time
filepath = str("audios/" + str(filename_base) + "_audiofiles")
filename = str(str(filepath) + "/" + str(filename_base) + ".wav")
filenamevideo = str("videos/" + str(filename_base) + ".mkv")


################################################################################

def split_and_transcribe_audio(filename, filepath):
    sound_file = AudioSegment.from_wav(filename)
    print(len(sound_file))
    iterations = len(sound_file)/3000
    roundlength = (len(sound_file)/1000)*1000
    left_over = roundlength-(iterations*3000)
    print str(iterations)
    print str(left_over)
    iteration = 1
    chunks = []
    captions = []
    r = sr.Recognizer()    
    while iteration <= iterations:
        clip = sound_file[(iteration*3000)-3000:iteration*3000]
        out_file = filepath + "/" + filename_base + "_chunk" + str(iteration) + ".wav"
        print("exporting", out_file)
        clip.export(out_file, format="wav")
        with sr.AudioFile(out_file) as source:
            framerate = 100
            audio = r.record(source)
            decoder = r.recognize_sphinx(audio, show_all=False)
        try:
            print("Sphinx thinks you said:  \n\n")
            print('"' + decoder + '"')
            captions.append((str(decoder), (iteration*3000)-3000, iteration*3000))
            print("\n\n")
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
        iteration = iteration + 1
        chunks.append(str(out_file))
    last_clip = sound_file[-left_over:]
    out_file_last = filepath + "/" + filename_base + "_chunk" + str(iterations + 1) + ".wav"
    chunks.append(str(out_file_last))
    print ("exporting", out_file_last)
    last_clip.export(out_file_last, format="wav")
    with sr.AudioFile(out_file) as source:
        framerate = 100
        audio = r.record(source)
        decoder = r.recognize_sphinx(audio, show_all=False)
    try:
        print("Sphinx thinks you said:  \n\n")
        print('"' + decoder + '"')
        captions.append((str(decoder), roundlength-left_over, roundlength))
        print("\n\n")
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    return (chunks, captions)
    
################################################################################

def convert_or_copy(filename_base, filepath):
    if source_file.endswith(".mp4"):
        print str(len(source_file)) + "MP4 \n\n\n\n\n\n\n\n\n\n"
        command2 = str("ffmpeg -i " + str(source_file) + " -vn " + str(filenamevideo))
        subprocess.check_output(command2, shell=True)
        command1 = str("ffmpeg -i " + str(source_file) + " -vn " + str(filename))
        subprocess.check_output(command1, shell=True)
    else:
        print "Not an MP4 \n\n\n\n\n"
        command1 = str("ffmpeg -i " + str(source_file) + " -vn " + str(filename))
        subprocess.check_output(command1, shell=True)

        
################################################################################

def google_recognize(source_file):
    r = sr.Recognizer()
    with sr.AudioFile(source_file) as source:
        audio = r.record(source)
    try:    
        print("Google thinks you said:  \n\n")
        print('"' + r.recognize_google(audio) + '"')
        print("\n\n")
    except sr.UnknownValueError:
        print("Google could not understand audio")
    except sr.RequestError as e:
        print("Could not complete request for Google Speech Recognition service; {0}".format(e))
        
################################################################################
        
def write_caption(source_file, captions, filename_base):
    source_video = VideoFileClip(source_file)
    source_video.set_duration(len(source_file))
    filename_convert = str("videos/" + str(filename_base) + "_converted.avi")
    source_video.write_videofile(filename_convert)
    for caption in captions:
        print caption
        video = VideoFileClip(filename_convert).subclip(caption[1], caption[2])
        print str(video)
        txt_clip = (TextClip(str(caption[0]), fontsize=18,color='white').set_position('center').set_duration(caption[2]-caption[1]))
        print str(txt_clip) 
        result = CompositeVideoClip([video, txt_clip])
        filename_out = str("videos/" + str(filename_base) + "_C.mp4")
        result.write_videofile(filename_out)
        

################################################################################
#########################Actual Script##########################################

if not os.path.exists(filepath):
    os.makedirs(filepath)
convert_or_copy(filename_base, filepath)
(clips, captions) = split_and_transcribe_audio(filename, filepath)
print captions
write_caption(source_file, captions, filename_base)        
        
        
        
        
        
        
        
        
        
