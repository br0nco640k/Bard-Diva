# BardLinux-Player

Python script that plays MIDI files in Final Fantasy XIV's Bard Performance Mode, akin to BardMusicPlayer, but for Linux!



#### To install dependencies:

| Debian-based distros        | Fedora                        | Arch Linux     | Void Linux                    |
|:---------------------------:|:-----------------------------:|:--------------:|:-----------------------------:|
| `apt-get install python-tk` | `dnf install python3-tkinter` | `pacman -S tk` | `xbps-install python3-tkinter` |

`pip install -r requirements.txt`



#### Before running:

Ensure keybindings are set as per [BardMusicPlayer's settings](https://bardmusicplayer.com/perf_settings.png).



#### Running:

- Open up Bard Performance Mode in FFXIV with instrument of choice

- Run `python play.py "path/To/MidiFile/song.midi"`

- Switch back to FFXIV in performance mode, and rock out

Playing will start after a 2 second delay. This can be updated in play.py, under the sleep(2) function.
