#!/usr/bin/env python3

# imports:
from tkinter import *
from tkinter import IntVar
from tkinter import filedialog
from _thread import start_new_thread
import mido 
from pyautogui import press
# Lets us hold notes by doing keyDown and keyUp:
from pyautogui import keyDown
from pyautogui import keyUp
import time as Time

# Some globals for adding a looping option to the GUI later on:
LoopSong = False # Set to True for song looping, will add a GUI option later
SinglePlay = False
QuitPlay = False

# We'll add gui option to set the delay time for window switching:
delay_time = 5
# For future use:
AllTracks = False
# Window geometry:
width = 900
height = 600
track_name=""


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
        123: "s",
        104: "m",
        92:  "n",
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
        123: "B --octave",
        104: "G# --octave",
        92:  "F# --ocatave",
    }

    return notes.get(frequency,
                     f"\t\t note NOT FOUND, frequency: {frequency}")

def play_midi(filename):
    global LoopSong
    global SinglePlay
    global QuitPlay
    QuitPlay = False
    print("Looping set to: ", LoopSong)
    # Import the MIDI file
    midi_file = mido.MidiFile(filename, clip=True)
    if midi_file.type == 3:
        print("Unsupported type.")
        app.action_label.config(text="Unsupported file type")
        exit(3)
    else:
        app.action_label.config(text="File loaded.")

    print(filename)
    # Wait time to switch window:
    for x in range(delay_time):
        print("playing in ", delay_time - x)
        app.action_label.config(text="Playing in " + str(delay_time - x))
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
                    app.action_label.config(text="Playing: " + frequency_to_readable_note(note_to_frequency(message.note)))
                else:
                    print("Waiting for next note")
                    app.action_label.config(text="Waiting for next note.")
            if QuitPlay:
                #print("Ending song.")
                SinglePlay = False
                LoopSong = False
                break
                #return None
        if (QuitPlay):
            SinglePlay = False
            LoopSong = False
            break
        if (SinglePlay):
            SinglePlay = False
        else:
            print("Looping song: ", filename)
            app.action_label.config(text="Looping song.")
    print("Ending song.")
    app.action_label.config(text="Ending song.")
    app.play_button.config(state='active')
    app.stop_button.config(state='disabled')

# The NEW GUI stuff begins here:

# Define the window:
class Main_Window(Tk):
    # main init:
    def __init__(self):
        #global LoopBox
        super().__init__()
        self.LoopBox = IntVar()
        self.title('Bard-Diva')
        self.geometry(str(width) + 'x' + str(height))
        # widgets here:
        self.label_title = Label(self, text = 'Bard Diva: MIDI player for FFXIV bards')
        self.label_title.pack()
        self.filename = Text(self, width=50, height=4)
        self.filename.pack()
        self.filename.config(state='disabled')
        self.file_button = Button(self, text="Open File", command=self.file)
        self.file_button.pack()
        self.action_label = Label(self, text="")
        self.action_label.pack()
        # Debug: this checkbox doesn't set the variable
        self.loop_song = Checkbutton(self,
                                     text="Loop Song",
                                     variable=self.LoopBox,
                                     onvalue=1,
                                     offvalue=0,
                                     height=2,
                                     width=10)
        self.loop_song.pack()
        self.play_button = Button(self, text="Play Song", command=self.play_song, state='disabled')
        self.play_button.pack()
        self.stop_button = Button(self, text="Stop Playing", command=self.stop_playing, state='disabled')
        self.stop_button.pack()

    def file(self):
        global track_name
        self.file_to_play = filedialog.askopenfilename(initialdir="",
                                                       title="Select MIDI file",
                                                       filetypes=[("MIDI files", "*.mid")])
        if self.file_to_play:
            self.filename.config(state='normal')
            self.filename.delete("1.0", END)
            self.filename.insert(END, self.file_to_play)
            track_name=self.file_to_play
            self.play_button.config(state="active")
            self.filename.config(state='disabled')
        
    def play_song(self):
        global LoopSong
        global SinglePlay
        self.action_label.config(text="Change to FFXIV window in the next 5 seconds.")
        print("Status of LoopBox var: ", self.LoopBox)
        if self.LoopBox.get() == 1:
            LoopSong = True
        else:
            SinglePlay = True
        start_new_thread(play_midi, (track_name, ))
        self.stop_button.config(state='active')
        self.play_button.config(state='disabled')
        #play_midi(track_name)

    def stop_playing(self):
        global QuitPlay
        global SinglePlay
        SinglePlay = False
        QuitPlay = True
        self.stop_button.config(state='disabled')
        self.play_button.config(state='active')

# Instantiate window:
app = Main_Window()
app.mainloop()
