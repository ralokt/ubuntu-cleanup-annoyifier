#!/usr/bin/python2

from subprocess import Popen
from subprocess import call
from os import listdir
from time import sleep
import random

def play_with_cvlc(files):
    call(["cvlc"]+files+["--play-and-exit"])

def play_with_cvlc_killafter(files, time):
    process = Popen(["cvlc"]+files+["--play-and-exit"])
    sleep(time)
    process.kill()

def play_with_espeak(files, lang):
    for i in files:
        call(["espeak", "-v", lang, "-f", i])

def shuffle_files(directory, first=0):
    files = [directory + "/" + f for f in listdir(directory)]
    random.shuffle(files)
    if first==0:
        return files
    else:
        return files[0:first]

if __name__ == "__main__":
    print(shuffle_files("samples"))
    play_with_espeak(shuffle_files("texts"), "de")

