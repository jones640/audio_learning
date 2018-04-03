#!/usr/bin/python2.7

import ffmpy as ffmpy
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
initialviddir = "/home/alex/audio_recognition/videos"
submit_time = datetime.now().strftime("%Y%m%d_%H%M")

ftypes = [
    ('Python code files', '*.py'), 
    ('Perl code files', '*.pl;*.pm'),  # semicolon trick
    ('Java code files', '*.java'), 
    ('C++ code files', '*.cpp;*.h'),   # semicolon trick
    ('Text files', '*.txt'), 
    ('All files', '*'), 
]

source_file = tkFileDialog.askopenfilename(parent=gui, initialdir=initialviddir, title= 'Select a video file to be analyzed', filetypes=ftypes)

init_filename_list = source_file.split('/')
init_filename = init_filename_list[-1]
filename_base_list = init_filename.split('.')
filename_base = filename_base_list[0]
filename = str("audios/" + str(filename_base) + "_" + submit_time + ".wav")

print(str(source_file))

print(str(filename))

command = str("ffmpeg -i " + str(source_file) + " -vn " + str(filename))
    
subprocess.call(command, shell=True)
