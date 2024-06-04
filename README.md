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

Ensure keybindings are set as per the following:
![image info](./perf_settings.png)
![image info](./tone_switching.jpg)

#### Running:

- Open up Bard Performance Mode in FFXIV with instrument of choice

- Run `python play.py` or `./play.py` and select the files in the GUI

- Switch back to FFXIV, and rock out

#### New features:

- Play all channels or just play a single channel, which is good for songs that work better with one or the other

- Selectable delay time in GUI

- Lists all channels and instruments assigned, including tone switches

- GUI implemented in Tkinter to fix license issues

- Guitar "tone switching" like Bard Music Player

- Ability to hold long notes (highly experimental right now)

#### Planned features:

- Ability to pause songs

- Ability to select an octave range target

- Ability to selectively enable or disable any channel

- Wayland option (for Linux users that have moved to Wayland that have issues)
