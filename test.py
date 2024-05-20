#!/usr/bin/env python3

import os.path
# tkinter will be used for our GUI as we phase out PySimpleGUI:
import tkinter as tk
# Do we actually need this (since we have ALL of tkinter above):
from tkinter import ttk
from _thread import start_new_thread
from glob import glob
# We're now just grabbing all of mido:
import mido 
from pyautogui import press
# Lets us hold notes by doing keyDown and keyUp:
from pyautogui import keyDown
from pyautogui import keyUp
# we're grabbing all of time now, because we need more of it later on:
import time as Time

# Some globals for adding a looping option to the GUI later on:
LoopSong = False # Set to True for song looping, will add a GUI option later
SinglePlay = False

# We'll add gui option to set the delay time for window switching:
delay_time = 5
# For future use:
AllTracks = False
# Window geometry:
width = 800
height = 500


def note_to_frequency(note):
    """
    Convert a MIDI note into a frequency (given in Hz):
    """
    return round(440 * 2**((note - 69) / 12))

def frequency_to_key(frequency):
    """
    Convert a frequency (given in Hz) into a key press:
    """
    notes = {
        1864: "j",
        1760: "8",
        1568: "5",
        1397: "4",
        1319: "3",
        1175: "2",
        1047: "8",
        988: "7",
        932: "j",
        880: "6",
        831: "h",
        784: "5",
        740: "g",
        698: "4",
        659: "3",
        622: "f",
        587: "2",
        554: "d",
        523: "1",
        494: "t",
        466: "c",
        440: "r",
        415: "x",
        392: "e",
        370: "z",
        349: "w",
        330: "q",
        311: "l",
        294: "0",
        277: "k",
        262: "9",
        247: "s",
        233: ".",
        220: "a",
        208: "m",
        196: "p",
        185: "n",
        175: "o",
        165: "i",
        156: "b",
        147: "u",
        139: "v",
        131: "y",
    }

    return notes.get(frequency,
                     f"\t\t keystroke NOT FOUND, frequency: {frequency}")

def frequency_to_readable_note(frequency):
    """
    Convert a frequency (given in Hz) into a readable note:
    """
    notes = {
        1864: "B flat +octave",
        1760: "C+1",
        1568: "G +octave",
        1397: "F +octave",
        1319: "E +octave",
        1175: "D +octave",
        1047: "C+1",
        988: "B +octave",
        932: "B flat +octave",
        880: "A +octave",
        831: "G# +octave",
        784: "G +octave",
        740: "F# +octave",
        698: "F +octave",
        659: "E +octave",
        622: "E flat +octave",
        587: "D +octave",
        554: "C# +octave",
        523: "C +octave",
        494: "B",
        466: "B flat",
        440: "A",
        415: "G#",
        392: "G",
        370: "F#",
        349: "F",
        330: "E",
        311: "E flat",
        294: "D",
        277: "C#",
        262: "C",
        247: "B -octave",
        233: "B flat -octave",
        220: "A -octave",
        208: "G# -octave",
        196: "G",
        185: "F# -octave",
        175: "F",
        165: "E",
        156: "E flat",
        147: "D",
        139: "C# -octave",
        131: "C",
    }

    return notes.get(frequency,
                     f"\t\t note NOT FOUND, frequency: {frequency}")

def read_files(folder):
    files = glob(os.path.join(folder, "*.mid*"))
    file_names = [os.path.basename(file) for file in files]
    return file_names

def play_midi(filename):
    global LoopSong
    global SinglePlay
    # Import the MIDI file
    midi_file = mido.MidiFile(filename, clip=True)
    if midi_file.type == 3:
        print("Unsupported type.")
        exit(3)

    print(filename)
    # Wait time to switch window:
    for x in range(delay_time):
        print("playing in ", delay_time - x)
        Time.sleep(1)

    # Some additional notes for future functionality:
    # midi_file.length will return the total playback time in seconds
    # midi_file.MidiTrack has sub properties that we can use to get track names, etc.

    # Play the MIDI file
    # Plays all tracks in the midi file, we may add the ability to focus
    # on a single track later on:
    while (LoopSong) or (SinglePlay):
        for message in midi_file.play():               
            if hasattr(message, "velocity"):
                if int(message.velocity) > 0:
                    key_to_play = frequency_to_key(note_to_frequency(message.note))
                    press(key_to_play)
                    print("Playing: " + frequency_to_readable_note(note_to_frequency(message.note)))
            if stop:
                print("Ending song.")
                SinglePlay = False
                break
                #return None
        if (stop):
            break
        if (SinglePlay):
            SinglePlay = False
        else:
            print("Looping song: ", filename)
    print("Ending song.")

# The NEW GUI stuff begins here:

# Define the window:
window = tk.Tk()
window.title('Bard-Diva')
window.geometry(str(width) + 'x' + str(height))
title_label = ttk.Label(master = window, text = 'Bard Diva: MIDI player for FFXIV bards')
title_label.pack()
window.mainloop()
