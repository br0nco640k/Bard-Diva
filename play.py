#!/usr/bin/env python3

from mido import MidiFile, MetaMessage
import sys
from pathlib import Path
from time import sleep
import ntpath
import pyautogui
from pyautogui import press
import PySimpleGUI as sg
import os.path
import _thread
import glob

def note_to_frequency(note):
    """
    Convert a MIDI note into a frequency (given in Hz)
    """
    return round(440 * 2 ** ((note - 69) / 12))

def frequency_to_key(frequency):
    """
    Convert a frequency (given in Hz) into a key press
    """
    notes = {
        1864: "j",
        1760: "8",
        1568: "5",
        1397: "4",
        1319: "3",
        1175: "2",
        1047: "8",
        988:  "7",
        932:  "j",
        880:  "6",
        831:  "h",
        784:  "5",
        740:  "g",
        698:  "4",
        659:  "3",
        622:  "f",
        587:  "2",
        554:  "d",
        523:  "1",
        494:  "t",
        466:  "c",
        440:  "r",
        415:  "x",
        392:  "e",
        370:  "z",
        349:  "w",
        330:  "q",
        311:  "l",
        294:  "0",
        277:  "k",
        262:  "9",
        247:  "s",
        233:  ".",
        220:  "a",
        208:  "m",
        196:  "p",
        185:  "n",
        175:  "o",
        165:  "i",
        156:  "b",
        147:  "u",
        139:  "v",
        131:  "y"
    }
    
    return notes.get(frequency,
    "\t\t keystroke NOT FOUND, frequency: " + str(frequency))


def read_files(folder):
    files = glob.glob(os.path.join(folder, "*.mid*"))
    file_names = [os.path.basename(file) for file in files]
    return file_names


def play_midi(filename):
    pyautogui.PAUSE = 0.05

    # Import the MIDI file
    midi_file = MidiFile(filename)
    if midi_file.type == 3:
        print("Unsupported type.")
        exit(3)

    # Wait 3 seconds to switch window
    sleep(3)

    # Play the MIDI file
    for message in midi_file.play():
        if hasattr(message, "velocity"):
            if int(message.velocity) > 0:
                press(frequency_to_key(note_to_frequency(message.note)))
        if stop == True:
            break
    refresh_window()
    

def refresh_window():
    window.refresh()
    window["-STOP-"].update(disabled=True)


## GUI

# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("Select the songs directory"),
        sg.In("", size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Selected file:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Button('Play', enable_events=True, key="-PLAY-", disabled=True)],
    [sg.Button('Stop', enable_events=True, key="-STOP-", disabled=True)]
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("BardLinux-Player", layout)

# Run the Event Loop

stop = False

while True:
    event, values = window.read()
    stop = False
    if event == "Exit" or event == sg.WIN_CLOSED:
        stop = True
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        window["-FILE LIST-"].update(read_files(values["-FOLDER-"]))
        window["-TOUT-"].update('')
        window["-PLAY-"].update(disabled=True)

    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(values["-FILE LIST-"][0])
            window["-PLAY-"].update(disabled=False)
        except:
            pass

    elif event == "-PLAY-": # Play button pressed
        window["-STOP-"].update(disabled=False)
        _thread.start_new_thread(play_midi,(filename,))

    elif event == "-STOP-":  # Stop button pressed
        stop = True
        window["-STOP-"].update(disabled=True)

window.close()
