# Bard-Diva

Python script that plays MIDI files in Final Fantasy XIV's Bard Performance Mode, akin to BardMusicPlayer, but for Linux (and other systems that support Python 3 and Tkinter)!

#### To install dependencies:

| Debian-based distros         | Fedora                        | Arch Linux     | Void Linux                     |
|:----------------------------:|:-----------------------------:|:--------------:|:------------------------------:|
| `apt-get install python3-tk` | `dnf install python3-tkinter` | `pacman -S tk` | `xbps-install python3-tkinter` |

| Windows 10/11                     | macOS                  |
|:---------------------------------:|:----------------------:|
| `winget search Python.Python`     | `brew install python`  |
| `then:`                           | `(requires homebrew)`  |
| `winget install Python.Python.x`  |

`pip install -r requirements.txt`

#### Wayland users:

- You must install ydotool to enable keypresses to be sent, as a workaround to Wayland's security protocols. In this case pyautogui is not used at all, and will not be imported at run time.

For Ubuntu/Debian/Mint/Pop!_OS:
`sudo apt-get install ydotool`

For Fedora/RHEL/Rocky/Alma:
`sudo dnf install ydotool`

For Arch Linux:
`sudo pacman -S ydotool`

- You'll need to have the systemd user service running to setup the virtual input device. You can set the service to automatically start up when you login and also start it now with:
`systemctl --user enable --now ydotool`

(This does not actually work on my system, so I'll be writing much better instructions for getting the ydotool service working soon!)

#### Before running:

Ensure keybindings are set as per the following:
![image info](./perf_settings.png)
![image info](./tone_switching.jpg)

#### Running:

- Open up Bard Performance Mode in FFXIV with instrument of choice

- Run `python play.py` or `./play.py` and select the files in the GUI. If you get errors about pyautogui, try using the Wayland instructions instead (above and below), which in theory should work on all Linux systems.

- On Wayland run `python play.py wayland` or `./play.py wayland` instead

- Switch back to FFXIV, and rock out

#### New features:

- Play all channels or just play a single channel, which is good for songs that work better with one or the other

- Selectable delay time in GUI

- Lists all channels and instruments assigned, including tone switches (works for MIDI files that have a properly encoded program_change to identify the instrument for each channel, and for files that are encoded for tone switching for Bard Music Player)

- GUI implemented in Tkinter to fix license issues

- Guitar "tone switching" like Bard Music Player

- Song progress bar

- Ability to hold long notes (highly experimental right now)

- Ability to select an octave range target

- Song looping

#### Planned features:

- Ability to pause songs

- Ability to selectively enable or disable any channel

- Wayland option (for Linux users that have moved to Wayland that have issues)

- Network synchronization for multi-box performance (using zeroconf, perhaps)

- Visual song analyzer, to disply distribution of notes across each octave from 0 to 8

I'll probably work on some of those extra features after I get through the Dawntrail story!

#### Some notes for Windows 10/11 and macOS:

- Windows requires the App Installer application from the Windows Store, which is usually installed by default, but on rare occassions is not installed, in order to use winget from the command line. After searching for Python.Python, you must install the precise listed version that you want to use according to it's ID.

- macOS command line example above requires Homebrew
