#!/usr/bin/env python3

# We're planning to move away from PySimpleGUI because of the
# licensing change (going "pro") to make things easier for the users
# because users shouldn't have to sign up for a license key or buy it
# just to play some bard songs. Maybe we can do this with straight Tkinter:
import PySimpleGUI as GUI
import Tkinter as Tk
import os.path
from _thread import start_new_thread
from glob import glob
# We'll evaluate pulling in other mido functions (or all of mido):
from mido import MidiFile
# We're phasing out press():
from pyautogui import press
# Lets us hold notes by doing keyDown and keyUp:
from pyautogui import keyDown
from pyautogui import keyUp
from time import sleep


def note_to_frequency(note):
    """
    Convert a MIDI note into a frequency (given in Hz)
    May need to tweak this to limit ourselves to just
    three octaves (also might need a way to select octave range desired):
    """
    return round(440 * 2**((note - 69) / 12))


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


def read_files(folder):
    files = glob(os.path.join(folder, "*.mid*"))
    file_names = [os.path.basename(file) for file in files]
    return file_names


def play_midi(filename):
    current_note = "000"
    # Import the MIDI file
    midi_file = MidiFile(filename)
    if midi_file.type == 3:
        print("Unsupported type.")
        exit(3)

    # Wait 3 seconds to switch window
    # In the future we'll make this user selectable at run time
    # instead of hard coding it:
    sleep(3)

    # Some additional notes for future functionality:
    # midi_file.length will return the total playback time in seconds
    # midi_file.MidiTrack has sub properties that we can use to get track names, etc.
    # We may switch to reading in all of the messages in the file, and then
    # parsing through them to gain much more control over playback, instead of
    # just letting mido play it, perhaps MUCH later on

    # Play the MIDI file
    # Plays all tracks in the midi file, we may add the ability to focus
    # on a single track later on:
    for message in midi_file.play():
        if hasattr(message, "velocity"):
            if int(message.velocity) > 0:
                # Fix me:
                # We need a way to track the current note
                # so that we can hold it instead of pulsing it:
                key_to_play = frequency_to_key(note_to_frequency(message.note))
                if current_note != key_to_play:
                    keyDown(key_to_play)
                    current_note = key_to_play
            else:
                # Release the key when we no longer have "velocity":
                if current_note != "000": # 000 is unused above, means we haven't picked a note yet
                    keyUp(current_note)
        if stop:
            break
    refresh_window()


def refresh_window():
    window.refresh()
    window["-STOP-"].update(disabled=True)


# GUI
# All of this will have to change as we port away from PySimpleGUI:

# Left column
file_list_column = [
    [
        GUI.Text("Select the songs directory"),
        GUI.In("", size=(25, 1), enable_events=True, key="-FOLDER-"),
        GUI.FolderBrowse(),
    ],
    [
        GUI.Listbox(values=[],
                    enable_events=True,
                    size=(40, 20),
                    key="-FILE LIST-")
    ],
]

# Right column
button_column = [
    [GUI.Text("Selected file:")],
    [GUI.Text(size=(40, 1), key="-TOUT-")],
    [GUI.Button("Play", enable_events=True, key="-PLAY-", disabled=True)],
    [GUI.Button("Stop", enable_events=True, key="-STOP-", disabled=True)],
]

# Full layout with
layout = [[
    GUI.Column(file_list_column),
    GUI.VSeperator(),
    GUI.Column(button_column),
]]

window = GUI.Window("Bard Diva", layout)

# Run the Event Loop

stop = False

while True:
    event, values = window.read()
    stop = False

    # Exit the event loop if it meets these conditions
    if event == "Exit" or event == GUI.WIN_CLOSED:
        stop = True
        break

    # List the files in the directory
    if event == "-FOLDER-":
        window["-FILE LIST-"].update(read_files(values["-FOLDER-"]))
        window["-TOUT-"].update("")
        window["-PLAY-"].update(disabled=True)

    # A file was chosen from the list
    elif event == "-FILE LIST-":
        try:
            filename = os.path.join(values["-FOLDER-"],
                                    values["-FILE LIST-"][0])
            window["-TOUT-"].update(values["-FILE LIST-"][0])
            window["-PLAY-"].update(disabled=False)
        except (FileNotFoundError, IndexError):
            pass

    # Play button pressed
    elif event == "-PLAY-":
        window["-STOP-"].update(disabled=False)
        start_new_thread(play_midi, (filename, ))

    # Stop button pressed
    elif event == "-STOP-":
        stop = True
        window["-STOP-"].update(disabled=True)

window.close()
