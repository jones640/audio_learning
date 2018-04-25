#!/usr/bin/python2.7

"""
Dependencies for this script include: pocketsphinx, pydub, speech_recognition, Tkinter, tkFileDialog, traceback, tkMessageBox, subprocess, os, sys, datetime, and time
"""

from pocketsphinx import *
from pydub import AudioSegment
from pytube import YouTube
from pydub.silence import split_on_silence
import speech_recognition as sr
#from SpeechRecognition import *
import Tkinter # Python GUI package
from Tkinter import *
import tkFileDialog # for Dialog Box
import traceback # for error checking
import tkMessageBox
import subprocess
import os, sys, time
from datetime import datetime

################################################################################

def download_video(URL):
    download_filename = str('youtube_video_' + submit_time)
    YouTube(URL).streams.first().download(filename=str(download_filename))
    return download_filename

################################################################################

def filesetup(filepath, source_file):
    #if all files are setup and libraries are installed then the script will run
    #Need to check for several things
    if not os.path.exists("transcription_temp_files"):
        os.makedirs("transcription_temp_files")
    if not os.path.exists("videos"):
        os.makedirs("videos")
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    if download_choice == "Y":
        commandmv2 = ("mv " + source_file + " videos/" + str(filename_base) + ".mp4")
        subprocess.check_output(commandmv2, shell=True)
        source_file = ("videos/" + str(filename_base) + ".mp4")
    elif download_choice == "N":
        commandcp1 = ("cp " + source_file + " videos/" + str(filename_base) + ".mp4")
        subprocess.check_output(commandcp1, shell=True)
        source_file = ("videos/" + str(filename_base) + ".mp4")
    return source_file

################################################################################

def convert_or_copy(filename_base, filepath):
    if source_file.endswith(".mp4"):
        command1 = str("ffmpeg -i " + str(source_file) + " -vn " + str(filename))
        subprocess.check_output(command1, shell=True)
    else:
        print "Not an MP4 \n\n\n\n\n"
        command1 = str("ffmpeg -i " + str(source_file) + " -vn " + str(filename))
        subprocess.check_output(command1, shell=True)
        
################################################################################

def split_and_transcribe_audio(filename, filepath):
    srtfile_path = filepath + "/" + filename_base + "_subtitles.txt"
    srtfile = open(srtfile_path, "w")
    sound_file = AudioSegment.from_wav(filename)
    iterations = len(sound_file)/3000
    total_run_time = len(sound_file)
    left_over = (total_run_time) - (iterations*3000)
    iteration = 1
    chunks = []
    captions = []
    r = sr.Recognizer()    
    running_time = 000
    while iteration <= iterations:
        clip = sound_file[(iteration*3000)-3000:iteration*3000]
        out_file = filepath + "/" + filename_base + "_chunk" + str(iteration) + ".wav"
        clip.export(out_file, format="wav")
        analysis_out_file = AudioSegment.from_wav(out_file)
        with sr.AudioFile(out_file) as source:
            framerate = 100
            audio = r.record(source)
            decoder = r.recognize_sphinx(audio, show_all=False)
        try:
            captions.append((str(decoder), (iteration*3000)-3000, iteration*3000))
            if len(sound_file) < 60000:
                shour = str(0)
                sminute = str(00)
                ssecond = ((running_time)/1000)
                smilli = (running_time - (ssecond*1000))
                running_time = (running_time + len(analysis_out_file))
                fhour = str(0)
                fminute = str(00)
                fsecond = ((running_time)/1000)
                fmilli = (running_time - (fsecond*1000))
            elif len(sound_file) < 3600000:
                shour = str(0)
                sminute = ((running_time)/60000)
                ssecond = (((running_time) - (sminute*60000))/1000)
                smilli = ((running_time) - (sminute*60000) - (ssecond*1000))
                running_time = (running_time + len(analysis_out_file))
                fhour = str(0)
                fminute = ((running_time)/60000)
                fsecond = (((running_time) - (fminute*60000))/1000)
                fmilli = ((running_time) - (fminute*60000) - (fsecond*1000))
            if sminute < 10:
                sminute = (str(0) + str(sminute))
            if ssecond < 10:
                ssecond = (str(0) + str(ssecond))
            if smilli < 1:
                smilli = str('000')
            elif smilli < 10:
                smilli = (str(00) + str(smilli))
            elif smilli < 100:
                smilli = (str(0) + str(smilli))
            if fminute < 10:
                fminute = (str(0) + str(fminute))
            if fsecond < 10:
                fsecond = (str(0) + str(fsecond))
            if fmilli < 1:
                fmilli = str('000')
            if fmilli < 10:
                fmilli = (str(00) + str(smilli))
            elif fmilli < 100:
                fmilli = (str(0) + str(smilli))
            srtfile.write(str(iteration) + "\n" + str(shour) + ":" + str(sminute) + ":" + str(ssecond) + "," + str(smilli) + " --> " + str(fhour) + ":" + str(fminute) + ":" + str(fsecond) + "," + str(fmilli) + "\n" + str(decoder) + "\n\n")
            print(str(iteration) + "\n" + str(shour) + ":" + str(sminute) + ":" + str(ssecond) + "," + str(smilli) + " --> " + str(fhour) + ":" + str(fminute) + ":" + str(fsecond) + "," + str(fmilli) + "\n" + str(decoder) + "\n")
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
            continue
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
            continue
        cleanup_cmd = "rm " + out_file
        subprocess.check_output(cleanup_cmd, shell=True)
        iteration = iteration + 1
    last_clip = sound_file[-left_over:]
    out_file_last = filepath + "/" + filename_base + "_chunk" + str(iterations + 1) + ".wav"
    chunks.append(str(out_file_last))
    last_clip.export(out_file_last, format="wav")
    analysis_out_file = AudioSegment.from_wav(out_file_last)
    with sr.AudioFile(out_file_last) as source:
        framerate = 100
        audio = r.record(source)
        decoder = r.recognize_sphinx(audio, show_all=False)
    try:
        captions.append((str(decoder), running_time, total_run_time))
        shour = str(0)
        sminute = ((running_time)/60000)
        ssecond = (((running_time) - (sminute*60000))/1000)
        smilli = ((running_time) - (sminute*60000) - (ssecond*1000))
        running_time = (running_time + len(analysis_out_file))
        fhour = str(0)
        fminute = ((running_time)/60000)
        fsecond = (((running_time) - (fminute*60000))/1000)
        fmilli = ((running_time) - (fminute*60000) - (fsecond*1000))
        if sminute < 10:
            sminute = (str(0) + str(sminute))
        if ssecond < 10:
            ssecond = (str(0) + str(ssecond))
        if smilli < 1:
            smilli = str('000')
        elif smilli < 10:
            smilli = (str(00) + str(smilli))
        elif smilli < 100:
            smilli = (str(0) + str(smilli))
        if fminute < 10:
            fminute = (str(0) + str(fminute))
        if fsecond < 10:
            fsecond = (str(0) + str(fsecond))
        if fmilli < 1:
            fmilli = str('000')
        if fmilli < 10:
            fmilli = (str(00) + str(smilli))
        elif fmilli < 100:
            fmilli = (str(0) + str(smilli))
        srtfile.write(str(iteration) + "\n" + str(shour) + ":" + str(sminute) + ":" + str(ssecond) + "," + str(smilli) + " --> " + str(fhour) + ":" + str(fminute) + ":" + str(fsecond) + "," + str(fmilli) + "\n" + str(decoder) + "\n\n")
        print(str(iteration) + "\n" + str(shour) + ":" + str(sminute) + ":" + str(ssecond) + "," + str(smilli) + " --> " + str(fhour) + ":" + str(fminute) + ":" + str(fsecond) + "," + str(fmilli) + "\n" + str(decoder) + "\n")
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    cleanup_cmd = "rm " + out_file_last
    subprocess.check_output(cleanup_cmd, shell=True)
    return (srtfile_path)
        
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

def video(name):
    for extension in ['.mp4', '.avi', '.mkv']:
        if name.endswith(extension):
            return True
    return False

################################################################################

def write_caption(filepath, filename_base):
    srtfile_path_orig = filepath + "/" + filename_base + "_subtitles.txt"
    srtfile_path_capt = filepath + "/" + filename_base + "_subtitles.srt"
    command3 = str("mv " + str(srtfile_path_orig) + " " + str(srtfile_path_capt))
    subprocess.check_output(command3, shell=True)
    command = 'ffmpeg -i ' + source_file + ' -i ' + srtfile_path_capt + ' -c:s mov_text -c:v copy -c:a copy ' + filenamevideo + '_c.mp4'
    if video(source_file):
        subprocess.check_output(command, shell=True)
    return srtfile_path_capt
        
################################################################################

def cleanup(filepath, srtfile_path_capt):
    if os.path.exists(srtfile_path_capt):
        command4 = str("mv " + srtfile_path_capt + " " + filenamevideo + "_subtitles.srt")
        subprocess.check_output(command4, shell=True)
    if os.path.exists(filename):
        command5 = str("rm " + filename)
        subprocess.check_output(command5, shell=True)
    if os.path.exists(filepath):
        os.rmdir(filepath)
    if os.path.exists("transcription_temp_files"):
        command6 = "rmdir transcription_temp_files"
        subprocess.check_output(command6, shell=True)

#########################Actual Script##########################################

gui = Tkinter.Tk()
gui.attributes("-topmost")
gui.withdraw()
initialdir = os.getcwd()
submit_time = datetime.now().strftime("%Y%m%d_%H%M")
ftypes = [('All files', '*')]
cwd = os.getcwd()
print("\n\n\n\n\n" + cwd + "\n\n\n\n\n") 
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

download_choice = raw_input("Do you need to download the video? (Y/N) ")
if download_choice == "Y":
    submitURL = raw_input("please enter URL: ")
    print("\n\n\n Now downloading video from: " + submitURL + " \n\n\n")
    download_filename = download_video(submitURL)
    filename_base = download_filename
    source_file = str(cwd + "/" + filename_base + ".mp4")

elif download_choice == "N":
    source_file_dirty = tkFileDialog.askopenfilename(parent=gui, initialdir=initialdir, title= 'Select a file to be analyzed', filetypes=ftypes)
    print("\n\n\n\n" + source_file_dirty + "\n\n\n\n")
    if " " in source_file_dirty:
        source_filecmd = source_file_dirty.replace(" ", "\ ")
        source_file = source_filecmd.replace("\342\200\223", "")
        source_file = source_file.replace("\ ", "_")
        commandmv1 = ("mv " + source_filecmd + " " + source_file)
        subprocess.check_output(commandmv1, shell=True)
    else:
        source_file = source_file_dirty
    print source_file
    init_filename_list = source_file.split('/')
    init_filename = init_filename_list[-1]
    filename_base_list = init_filename.split('.')
    filename_base = filename_base_list[0] + "_" + submit_time

filepath = str("transcription_temp_files/" + str(filename_base) + "_audiofiles")
filename = str(str(filepath) + "/" + str(filename_base) + ".wav")
filenamevideo = str("videos/" + str(filename_base))


#    if os.path.exists(home/audio_learning):
#        return True    
#    return False

################################################################################


source_file = filesetup(filepath, source_file)
convert_or_copy(filename_base, filepath)
srtfile_path = split_and_transcribe_audio(filename, filepath)
srtfile_path_capt = write_caption(filepath, filename_base)        
cleanup(filepath, srtfile_path_capt)        
        
        
        
        
        
        
        
