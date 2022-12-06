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


def readFiles(f):
    folder = f
    try:
        # Get list of files in folder
        file_list = os.listdir(folder)
    except:
        file_list = []

    fnames = [
        f
        for f in file_list
        if os.path.isfile(os.path.join(folder, f))
        and f.lower().endswith((".mid", ".midi"))
    ]
    return fnames

def playMidi(filename):
    pyautogui.PAUSE = 0.05
    # Import the MIDI file...
    mid = MidiFile(filename)
    if mid.type == 3:
        print("Unsupported type.")
        exit(3)

    # wait 3 seconds to switch window
    sleep(3)

    try:
        for msg in mid.play():
            if hasattr(msg, 'velocity'):
                #print(msg)
                window.refresh()
                if int(msg.velocity) > 0:
                    press(frequency_to_key(note_to_frequency(msg.note)))
            if stop == True:
                break
        window["-STOP-"].update(disabled=True)
    except KeyboardInterrupt:
        print('quit')
        sys.exit()

## GUI

# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("Choose Songs Folder"),
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
    [sg.Button('Play !', enable_events=True, key="-PLAY-", disabled=True)],
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

window = sg.Window("BardMac-sicPlayer", layout)

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
        window["-FILE LIST-"].update(readFiles(values["-FOLDER-"]))
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
        _thread.start_new_thread(playMidi,(filename,))

    elif event == "-STOP-":  # Stop button pressed
        stop = True
        window["-STOP-"].update(disabled=True)

window.close()
