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

#### Before running:

Ensure keybindings are set as per [BardMusicPlayer's settings](https://bardmusicplayer.com/perf_settings.png).
![image info](./perf_settings.png)

#### Running:

- Open up Bard Performance Mode in FFXIV with instrument of choice

- Run `python play.py` or `./play.py` and select the files in the GUI

- Switch back to FFXIV, and rock out

Playing will start after a 5 second delay. This can be updated in play.py, under the sleep() function.

Now has the ability to list all channels, with assigned instrument. Can select a single channel or play all channels.

Code has been ported from PySimpleGUI to Tkinter. Now includes the ability to loop songs.

#### Planned features:

- Ability to pause songs

- Ability to hold long notes

- Ability to select an octave range target

- Guitar "tone switching" like Bard Music Player

- Wayland option (for Linux users that have moved to Wayland that have issues)
