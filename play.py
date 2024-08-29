#!/usr/bin/env python3

# imports:
from tkinter import *
from tkinter import IntVar
from tkinter import filedialog
from _thread import start_new_thread
from tkinter import ttk
import mido
import time as Time
import sys

# Global needed for conditionals
UseWayland = False

# Conditional imports:
if len(sys.argv) > 1:
    Argument1 = sys.argv[1]
    if Argument1 == 'wayland':
        UseWayland = True
if (UseWayland):
    print("Setting Wayland mode.")
    import subprocess
else:
    from pyautogui import press
    # Lets us hold notes by doing keyDown and keyUp:
    from pyautogui import keyDown
    from pyautogui import keyUp


################################################################################
# New GUI and features by br0nco640k
# Thanks to angrymarker, realAbitbol and sirkhancision for their commits!
################################################################################

# Some globals for the looping option:
LoopSong = False # Set to True for song looping, will add a GUI option later
SinglePlay = False
QuitPlay = False
HoldNotes = False
HeldKeys = ""

# Gui option to set the delay time for window switching:
delay_time = 5
# For future use:
AllTracks = False
GuitarToneSwitch = False
ChannelToPlay = 0
OctaveTarget = 0
# Window geometry:
width = 900
height = 1300 # This will be troublesome for many users, needs to be fixed for 1080P displays
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
    # Different sets for different octave targets:
    notes_minus1 = { # I'll need to check these during debugging:
        7902: "7",
        7459: "j",
        7040: "6",
        6645: "h",
        6272: "5",
        5920: "g",
        5588: "4",
        5274: "3",
        4978: "f",
        4699: "2",
        4435: "d",
        4186: "1",
        3951: "7",
        3729: "j",
        3520: "6",
        3322: "h",
        3136: "5",
        2960: "g",
        2794: "4",
        2637: "3",
        2489: "f",
        2349: "2",
        2217: "d",
        2093: "1",
        1976: "7",
        1865: "j", # may sometimes hit as 1864! Apparently round() is buggy
        1864: "j",
        1760: "6",
        1661: "h",
        1568: "5",
        1480: "g",
        1397: "4",
        1319: "3",
        1245: "f",
        1175: "2",
        1109: "d",
        1047: "1",
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
        494: "7",
        466: "j",
        440: "6",
        415: "h",
        392: "5",
        370: "g",
        350: "4",
        330: "3",
        311: "f",
        294: "2",
        277: "d",
        262: "1",
        247: "t",
        233: "c",
        220: "r",
        208: "x",
        196: "e",
        185: "z",
        175: "w",
        165: "q",
        156: "l",
        147: "0",
        139: "k",
        131: "9",
        123: "s",
        117: ",",
        110: "a",
        104: "m",
        98:  "p",
        93:  "n",
        87:  "o",
        82:  "i",
        78:  "b",
        73:  "u",
        70:  "v",
        65:  "y",
        62:  "s",
        58:  ",",
        55:  "a",
        52:  "m",
        49:  "p",
        46:  "n",
        44:  "o",
        41:  "i",
        39:  "b",
        37:  "u",
        35:  "v",
        33:  "y",
        31:  "s",
        29:  ",",
        28:  "a",
        26:  "m",
        25:  "p",
        23:  "n",
        22:  "o",
        21:  "i",
        19:  "b",
        18:  "u",
        17:  "v",
        16:  "y",
    }

    notes_zero = {
        1864: "j",
        1760: "8",
        1568: "5",
        1397: "4",
        1319: "3",
        1175: "2",
        1047: "8",
        1109: "d",
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
        233: ",",
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
        110: "a",
        104: "m",
        98:  "p",
        92:  "n",
        82:  "i",
        73:  "u",
        65:  "y",
        62:  "s",
        55:  "a",
        49:  "p",
    }

    notes_plus1 = {
        7902: "7",
        7459: "j",
        7040: "6",
        6645: "h",
        6272: "5",
        5920: "g",
        5588: "4",
        5274: "3",
        4978: "f",
        4699: "2",
        4435: "d",
        4186: "1",
        3951: "7",
        3729: "j",
        3520: "6",
        3322: "h",
        3136: "5",
        2960: "g",
        2794: "4",
        2637: "3",
        2489: "f",
        2349: "2",
        2217: "d",
        2093: "1",
        1976: "7",
        1865: "j", # may sometimes hit as 1864! Apparently round() is buggy
        1864: "j",
        1760: "6",
        1661: "h",
        1568: "5",
        1480: "g",
        1397: "4",
        1319: "3",
        1245: "f",
        1175: "2",
        1109: "d",
        1047: "1",
        988: "t",
        932: "c",
        880: "r",
        831: "x",
        784: "e",
        740: "z",
        698: "w",
        659: "q",
        622: "l",
        587: "0",
        554: "k",
        523: "9",
        494: "s",
        466: ",",
        440: "a",
        415: "m",
        392: "p",
        370: "n",
        349: "o",
        330: "i",
        311: "b",
        294: "u",
        277: "v",
        262: "y",
        247: "s",
        233: ",",
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
        117: ",",
        110: "a",
        104: "m",
        98:  "p",
        93:  "n",
        87:  "o",
        82:  "i",
        78:  "b",
        73:  "u",
        70:  "v",
        65:  "y",
        62:  "s",
        58:  ",",
        55:  "a",
        52:  "m",
        49:  "p",
        46:  "n",
        44:  "o",
        41:  "i",
        39:  "b",
        37:  "u",
        35:  "v",
        33:  "y",
        31:  "s",
        29:  ",",
        28:  "a",
        26:  "m",
        25:  "p",
        23:  "n",
        22:  "o",
        21:  "i",
        19:  "b",
        18:  "u",
        17:  "v",
        16:  "y",
    }

    match OctaveTarget:
        case -1:
            return notes_minus1.get(frequency,
                     f"\t\t keystroke NOT FOUND, frequency: {frequency}")
        case 0:
            return notes_zero.get(frequency,
                     f"\t\t keystroke NOT FOUND, frequency: {frequency}")
        case 1:
            return notes_plus1.get(frequency,
                     f"\t\t keystroke NOT FOUND, frequency: {frequency}")
        case _:
            return notes_zero.get(frequency,
                     f"\t\t keystroke NOT FOUND, frequency: {frequency}")

def program_to_instrument_name(program):

    programs = {
        0: "Grand Piano",
        1: "Bright Piano",
        2: "Electric Grand Piano",
        3: "Honky-tonk Piano",
        4: "Electric Piano 1",
        5: "Electric Piano 2",
        6: "Harpsichord",
        7: "Clavinet",
        11: "Vibraphone",
        16: "Drawbar Organ",
        14: "Tubular Bells",
        19: "Church Organ",
        22: "Harmonica",
        24: "Accoustic Guitar",
        25: "Accoustic Guitar",
        26: "Electric Guitar",
        27: "Electric Guitar (clean)",
        28: "Electric Guitar (muted)",
        29: "Overdriven Guitar",
        30: "Distortion Guitar",
        31: "Guitar Harmonics",
        32: "Accoustic Bass",
        33: "Electric Bass (finger)",
        34: "Fretless Bass",
        35: "Fretless Bass",
        36: "Slap Bass 1",
        37: "Slap Bass 2",
        38: "Synth Bass 1",
        39: "Synth Bass 2",
        40: "Violin",
        41: "Viola",
        42: "Cello",
        44: "Tremolo Strings",
        45: "Pizzicato Strings",
        46: "Orchestral Harp",
        47: "Timpani",
        48: "String Ensemble 1",
        49: "String Ensemble 2",
        50: "Synth Strings 1",
        51: "Synth Strings 2",
        52: "Choir Aahs",
        53: "Voice Oohs",
        54: "Synth Choir",
        56: "Trumpet",
        57: "Trombone",
        58: "Tuba",
        60: "French Horn",
        61: "Brass Section",
        64: "Soprano Sax",
        65: "Alto Sax",
        66: "Tenor Sax",
        67: "Baritone Sax",
        68: "Oboe",
        69: "English Horn",
        70: "Bassoon",
        71: "Clarinet",
        72: "Piccolo",
        73: "Flute",
        74: "Recorder",
        75: "Pan Flute",
        90: "Pad 3 (polysynth)",
        93: "Pad 6 (mettalic)",
        95: "Pad 8 (sweep)",
        98: "FX 3 (crystal)",
        104: "Sitar",
        105: "Banjo",
        110: "Fiddle",
        117: "Melodic Tom",
    }

    return programs.get(program,
                     f"\t\t NOT FOUND: {program}")

def frequency_to_readable_note(frequency):
    """
    Convert a frequency (given in Hz) into a readable note:
    """
    notes = {
        1864: "B flat Octave 6",
        1760: "A Octave 6",
        1568: "G Octave 6",
        1397: "F Octave 6",
        1319: "E Octave 6",
        1175: "D Octave 6",
        1109: "C# Octave 6",
        1047: "C Octave 6",
        988: "B Octave 5",
        932: "B flat Octave 5",
        880: "A Octave 5",
        831: "G# Octave 5",
        784: "G Octave 5",
        740: "F# Octave 5",
        698: "F Octave 5",
        659: "E Octave 5",
        622: "E flat Octave 5",
        587: "D Octave 5",
        554: "C# Octave 5",
        523: "C Octave 5",
        494: "B Octave 4",
        466: "B flat Octave 4",
        440: "A Octave 4",
        415: "G# Octave 4",
        392: "G Octave 4",
        370: "F# Octave 4",
        349: "F Octave 4",
        330: "E Octave 4",
        311: "E flat Octave 4",
        294: "D Octave 4",
        277: "C# Octave 4",
        262: "C Octave 4",
        247: "B Octave 3",
        233: "B flat Octave 3",
        220: "A Octave 3",
        208: "G# Octave 3",
        196: "G Octave 3",
        185: "F# Octave 3",
        175: "F Octave 3",
        165: "E Octave 3",
        156: "E flat Octave 3",
        147: "D Octave 3",
        139: "C# Octave 3",
        131: "C Octave 3",
        123: "B Octave 2",
        117: "B flat Octave 2",
        110: "A Octave 2",
        104: "G# Octave 2",
        98:  "G Octave 2",
        92:  "F# Octave 2", # should round to 93 instead, round() bug?
        87:  "F Octave 2",
        82:  "E Octave 2",
        78:  "E flat Octave 2",
        73:  "D Octave 2",
        65:  "C Octave 2",
        62:  "B Octave 1",
        55:  "A Octave 1",
        49:  "G Octave 1", # We're missing quite a few here still
        31:  "B Octave 0",
    }

    return notes.get(frequency,
                     f"\t\t note NOT FOUND, frequency: {frequency}")

def play_midi(filename):
    global LoopSong
    global SinglePlay
    global QuitPlay
    global AllTracks
    global ChannelToPlay
    global HeldKeys
    global HoldNotes
    global UseWayland
    QuitPlay = False
    print("Looping set to: ", LoopSong)
    print("Playing channel:", ChannelToPlay)
    print('Wayland mode: ', UseWayland)
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

    # Play the MIDI file:
    start_time = Time.time()
    while (LoopSong) or (SinglePlay):
        for message in midi_file.play():
            current_time = Time.time()
            elapsed_time = (current_time - start_time)
            # Set our new progress_bar widget:
            app.progress_bar['value'] = elapsed_time/float(midi_file.length) * 100
            app.update()
            # program_change is used for assigning an instrument to a channel.
            # Bard Music Player can also use them in the middle of a song
            # for guitar tone switching:
            if message.type == 'program_change':
                print("Program change detected.")
                # Tone switching:
                print(GuitarToneSwitch)
                if (GuitarToneSwitch):
                    print(message)
                    instrument = message.program
                    match int(instrument):
                        case 24:
                            if UseWayland:
                                subprocess.run(f'/usr/bin/ydotool type -d 512 {"="}', shell=True)
                            else:
                                press("=")
                            print("Switching to clean guitar mode.")
                            app.action_label.config(text="Switching to clean guitar mode.")
                        case 25:
                            if UseWayland:
                                subprocess.run(f'/usr/bin/ydotool type -d 512 {"="}', shell=True)
                            else:
                                press("=")
                            print("Switching to clean guitar mode.")
                            app.action_label.config(text="Switching to clean guitar mode.")
                        case 26:
                            if UseWayland:
                                subprocess.run(f'/usr/bin/ydotool type -d 512 {"="}', shell=True)
                            else:
                                press("=")
                            print("Switching to clean guitar mode.")
                            app.action_label.config(text="Switching to clean guitar mode.")
                        case 27:
                            if UseWayland:
                                subprocess.run(f'/usr/bin/ydotool type -d 512 {"="}', shell=True)
                            else:
                                press("=")
                            print("Switching to clean guitar mode.")
                            app.action_label.config(text="Switching to clean guitar mode.")
                        case 28:
                            if UseWayland:
                                subprocess.run(f'/usr/bin/ydotool type -d 512 {"[=]"}', shell=True)
                            else:
                                press("[")
                            print("Switching to muted guitar mode.")
                            app.action_label.config(text="Switching to muted guitar mode.")
                        case 29:
                            if UseWayland:
                                subprocess.run(f'/usr/bin/ydotool type -d 512 {"-"}', shell=True)
                            else:
                                press("-")
                            print("Switching to overdriven guitar mode.")
                            app.action_label.config(text="Switching to overdriven guitar mode.")
                        case 30:
                            if UseWayland:
                                subprocess.run(f'/usr/bin/ydotool type -d 512 {"]"}', shell=True)
                            else:
                                press("]")
                            print("Switching to distortion guitar mode.")
                            app.action_label.config(text="Switching to distortion guitar mode.")
                        case 31:
                            if UseWayland:
                                subprocess.run(f'/usr/bin/ydotool type -d 512 {";"}', shell=True)
                            else:
                                press(";")
                            print("Switching to harmonics guitar mode.")
                            app.action_label.config(text="Switching to harmonics guitar mode.")
                        case _:
                            pass
            # This option is very experimental, and will get more work later on:
            if (HoldNotes):
                if message.type == 'note_on':
                    if AllTracks == False and int(message.channel) == ChannelToPlay:
                            key_to_play = frequency_to_key(note_to_frequency(message.note))
                            # Here we're releasing all previous keys:
                            while (len(HeldKeys) > 0):
                                tempkey = HeldKeys[0]
                                keyUp(tempkey)
                                HeldKeys = HeldKeys[1:]
                                #print(len(HeldKeys))
                                if QuitPlay:
                                    #print("Ending song.")
                                    SinglePlay = False
                                    LoopSong = False
                                    break
                            keyDown(key_to_play)
                            # Adding the newly held key to our "character array", aka our string:
                            HeldKeys += key_to_play
                            #print(message)
                            print("Ch: " + str(message.channel) + " Note: " + frequency_to_readable_note(note_to_frequency(message.note)))
                            app.action_label.config(text="Ch: " + str(message.channel) + " Note: " + frequency_to_readable_note(note_to_frequency(message.note)))
                    elif AllTracks == True:
                            key_to_play = frequency_to_key(note_to_frequency(message.note))
                            # Here we're releasing all previous keys:
                            while (len(HeldKeys) > 0):
                                tempkey = HeldKeys[0]
                                keyUp(tempkey)
                                HeldKeys = HeldKeys[1:]
                                #print(len(HeldKeys))
                                if QuitPlay:
                                    #print("Ending song.")
                                    SinglePlay = False
                                    LoopSong = False
                                    break
                            keyDown(key_to_play)
                            # Adding the newly held key to our "character array", aka our string:
                            HeldKeys += key_to_play
                            print("Ch: " + str(message.channel) + " Note: " + frequency_to_readable_note(note_to_frequency(message.note)))
                            #print(message)
                            app.action_label.config(text="Ch: " + str(message.channel) + " Note: " + frequency_to_readable_note(note_to_frequency(message.note)))
                if message.type == 'note_off':
                    key_to_release = frequency_to_key(note_to_frequency(message.note))
                    if len(key_to_release) > 1:
                        pass
                    else:
                        # We also need to find it in our held keys array and remove it
                        print("Releasing key")
                        keyUp(key_to_release)

            else:
                if hasattr(message, "velocity"):
                    if int(message.velocity) > 0:
                        # New single channel option:
                        if AllTracks == False and int(message.channel) == ChannelToPlay:
                            key_to_play = frequency_to_key(note_to_frequency(message.note))
                            if UseWayland:
                                subprocess.run(f'/usr/bin/ydotool type -d 512 {key_to_play}', shell=True)
                            else:
                                press(key_to_play)
                            print("Ch: " + str(message.channel) + " Note: " + frequency_to_readable_note(note_to_frequency(message.note)))
                            app.action_label.config(text="Ch: " + str(message.channel) + " Note: " + frequency_to_readable_note(note_to_frequency(message.note)))

                        # This is the original play option, which is well tested:
                        elif AllTracks == True:
                            key_to_play = frequency_to_key(note_to_frequency(message.note))
                            if UseWayland:
                                subprocess.run(f'/usr/bin/ydotool type -d 512 {key_to_play}', shell=True)
                            else:
                                press(key_to_play)
                            print("Ch: " + str(message.channel) + " Note: " + frequency_to_readable_note(note_to_frequency(message.note)))
                            app.action_label.config(text="Ch: " + str(message.channel) + " Note: " + frequency_to_readable_note(note_to_frequency(message.note)))
                        
            if QuitPlay:
                SinglePlay = False
                LoopSong = False
                break

        if (QuitPlay):
            SinglePlay = False
            LoopSong = False
            print("Playback stopped.")
            HoldNotes = False
            # Here we need to make sure that EVERY remaining held key gets released:
            while (len(HeldKeys) > 0):
                tempkey = HeldKeys[0]
                keyUp(tempkey)
                HeldKeys = HeldKeys[1:]
            break
        if (SinglePlay):
            SinglePlay = False
        else:
            print("Looping song: ", filename)
            start_time = Time.time()
            current_time = Time.time()
            elapsed_time = 0.0
            app.action_label.config(text="Looping song.")
            app.progress_bar['value'] = 0.0
            app.update()
    print("Ending song.")
    app.action_label.config(text="Ending song.")
    app.play_button.config(state='active')
    app.stop_button.config(state='disabled')
    #app.progress_bar.step(0.0)
    QuitPlay = False

# The NEW GUI stuff begins here:

# Define the window:
class Main_Window(Tk):
    # main init:
    def __init__(self):
        super().__init__()
        self.LoopBox = IntVar()
        self.ToneSwitch = IntVar()
        self.AllTracks = IntVar()
        self.LongNotes = IntVar()
        self.title('Bard Diva')
        self.geometry(str(width) + 'x' + str(height))
        # widgets here:
        self.label_title = Label(self, text = 'Bard Diva: MIDI player for FFXIV bards')
        self.label_title.pack()
        self.filename = Text(self, width=50, height=4)
        self.filename.pack(pady=10)
        self.filename.config(state='disabled')
        self.file_button = Button(self, text="Open File", command=self.file)
        self.file_button.pack(pady=10)
        self.action_label = Label(self, text="Not playing.", height=1)
        self.action_label.pack(pady=10)
        self.loop_song = Checkbutton(self,
                                     text="Loop Song",
                                     variable=self.LoopBox,
                                     onvalue=1,
                                     offvalue=0,
                                     height=1,
                                     width=10)
        self.loop_song.pack(pady=10)
        self.hold_long_notes = Checkbutton(self,
                                     text="Hold long notes (experimental)",
                                     variable=self.LongNotes,
                                     onvalue=1,
                                     offvalue=0,
                                     height=1,
                                     width=25)
        self.hold_long_notes.pack(pady=10)
        self.tone_switching = Checkbutton(self,
                                     text="Tone switching (guitar)",
                                     variable=self.ToneSwitch,
                                     onvalue=1,
                                     offvalue=0,
                                     height=1,
                                     width=20)
        self.tone_switching.pack(pady=10)
        self.tone_switching.select()
        self.play_all = Checkbutton(self,
                                     text="Play all channels",
                                     variable=self.AllTracks,
                                     onvalue=1,
                                     offvalue=0,
                                     height=1,
                                     width=14)
        self.play_all.pack(pady=10)
        self.play_all.select()
        self.channel_label = Label(self, text = 'Channel to play:')
        self.channel_label.pack()
        self.channel_to_play = Spinbox(self, from_=0, to=15)
        self.channel_to_play.pack(pady=10)
        self.octave_label = Label(self, text = 'Octave target:')
        self.octave_label.pack(pady=10)
        octave_range = StringVar(self)
        self.octave_spinner = Spinbox(self, from_=-1, to=1, textvariable=octave_range)
        self.octave_spinner.pack(pady=10)
        octave_range.set('0')
        self.delay_label = Label(self, text="Time to delay playback:")
        self.delay_label.pack(pady=10)
        playback_delay = StringVar(self)
        self.delay_spinner = Spinbox(self, from_=1, to=10, textvariable=playback_delay)
        self.delay_spinner.pack(pady=10)
        playback_delay.set('5')
        self.play_button = Button(self, text="Play Song", command=self.play_song, state='disabled')
        self.play_button.pack(pady=10)
        self.stop_button = Button(self, text="Stop Playing", command=self.stop_playing, state='disabled')
        self.stop_button.pack()
        self.progress_bar = ttk.Progressbar(length=800)
        self.progress_bar.pack(pady=10)
        # progress_bar.step(float) to set current song progress
        self.label_channels = Label(self, text = 'Instrument channels in file:')
        self.label_channels.pack()
        self.channel_list = Text(self, width=50, height=7)
        self.channel_list.pack(pady=10)
        self.channel_list.config(state='disabled')

    def file(self):
        global track_name
        TracksDetected = {}
        self.file_to_play = filedialog.askopenfilename(initialdir="",
                                                       title="Select MIDI file",
                                                       filetypes=[("MIDI files", "*.mid")])
        if self.file_to_play:
            self.progress_bar['value'] = 0.0
            self.update()
            self.filename.config(state='normal')
            self.filename.delete("1.0", END)
            self.filename.insert(END, self.file_to_play)
            track_name=self.file_to_play
            self.play_button.config(state="active")
            self.filename.config(state='disabled')
            midi_file = mido.MidiFile(track_name, clip=True)
            print(midi_file.length)
            self.channel_list.config(state='normal')
            self.channel_list.delete("1.0", END)
            freq_total = 0
            note_count = 0
            for msg in midi_file:
                if msg.type == "note_on":
                    # If we have a note_on, then the channel it occurs on is used:
                    TracksDetected[int(msg.channel)] = True                        
                    freq_total += note_to_frequency(msg.note)
                    note_count += 1
                # a program_change for each channel to identify the intended instrument for that channel:
                if msg.type == 'program_change': # Every program change sets a channel to an instrument type
                    # We can use that channel and program data to determine the type of instrument for that track
                    # and we can populate an options list for them all, by instrument name
                    self.channel_list.insert(END, "Chan: " + str(msg.channel) + " Inst: " + program_to_instrument_name(msg.program) + "\n")
            keylist = TracksDetected.keys()
            self.channel_list.insert(END, "Channels detected: " + str(keylist) + "\n")
            avg_note = round(freq_total/note_count)
            if (avg_note <= 247):
                self.channel_list.insert(END, "Recommended octave: -1\n")
            elif (avg_note <= 494):
                self.channel_list.insert(END, "Recommended octave: 0\n")
            else:
                self.channel_list.insert(END, "Recommended octave: +1\n")
            self.channel_list.insert(END, "Average note frequency: " + str(avg_note) + "\n")
            self.channel_list.config(state='disabled')
        
    def play_song(self):
        global LoopSong
        global SinglePlay
        global AllTracks
        global ChannelToPlay
        global delay_time
        global GuitarToneSwitch
        global HoldNotes
        global OctaveTarget
        self.progress_bar['value'] = 0.0
        self.update()
        # How long we'll wait before playback begins, so the user has time to switch
        # back over to FFXIV:
        delay_time = int(self.delay_spinner.get())
        self.action_label.config(text="Change to FFXIV window in the next " + self.delay_spinner.get() + " seconds.")
        if self.LongNotes.get() == 1:
            HoldNotes = True
        else:
            HoldNotes = False
        if self.LoopBox.get() == 1:
            LoopSong = True
            SinglePlay = False
            print("Looping enabled.")
        else:
            SinglePlay = True
            LoopSong = False
            print("Looping disabled.")
        if self.AllTracks.get() == 1:
            AllTracks = True
        else:
            ChannelToPlay = int(self.channel_to_play.get())
            AllTracks = False
        if self.ToneSwitch.get() == 1:
            GuitarToneSwitch = True
        else:
            GuitarToneSwitch = False
        OctaveTarget = int(self.octave_spinner.get())
        start_new_thread(play_midi, (track_name, ))
        self.stop_button.config(state='active')
        self.play_button.config(state='disabled')

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
