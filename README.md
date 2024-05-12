# BardLinux-Player

Python script that plays MIDI files in Final Fantasy XIV's Bard Performance Mode, akin to BardMusicPlayer, but for Linux!

#### To install dependencies:

| Debian-based distros         | Fedora                        | Arch Linux     | Void Linux                     |
|:----------------------------:|:-----------------------------:|:--------------:|:------------------------------:|
| `apt-get install python3-tk` | `dnf install python3-tkinter` | `pacman -S tk` | `xbps-install python3-tkinter` |

`pip install -r requirements.txt`

#### Before running:

Ensure keybindings are set as per [BardMusicPlayer's settings](https://bardmusicplayer.com/perf_settings.png).
![image info](./perf_settings.png)

#### Running:

- Open up Bard Performance Mode in FFXIV with instrument of choice

- Run `python play.py` or `./play.py` and select the files in the GUI

- Switch back to FFXIV, and rock out

Playing will start after a 3 second delay. This can be updated in play.py, under the sleep(3) function.

The intended purpose of this new fork is to port the GUI away from pysimplegui, and to add some additional features.
