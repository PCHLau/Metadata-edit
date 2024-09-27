# Metadata-edit

## Description

Metadata-edit is a package for downloading mp3 music files from youtube and tagging them with tags personalised to my preference. FOR PERSONAL USE ONLY.

It has the following main functions:

* Pulls audio (in mp3 format) and metadata from youtube using the [yt-dlp](https://github.com/yt-dlp/yt-dlp) module
* Uses [mutagen](https://github.com/quodlibet/mutagen) to add including the following
    1. Standard tags included in yt-dlp download, like title, artists, url, description, etc.
    2. Thumbnail, also obtained from yt-dlp, and cropped into appropriate square size
    3. Adds option to define mood tags according to user preference with `-m angry sad`
    4. Allows user to define what media the music came from with `-s Lord of the Rings`
    5. Adds lyrics (synced and unsynced), obtained using [syncedlyrics](https://github.com/moehmeni/syncedlyrics), with Netease, Musixmatch, and lrclib as sources
        * Uses [ytmusicapi](https://github.com/sigma67/ytmusicapi) to obtain lyrics if above sources yield nothing
    6. Autotranslates lyrics to Japanese if prompted with `-j`, uses [pykakasi](https://codeberg.org/miurahr/pykakasi)
    7. Uses Spotify web API through [spotipy](https://github.com/spotipy-dev/spotipy) to obtain track number and genres

Note: All formatting and ID3 tag designation have been designed around my preferences and compatibility with MusicBee and Apple Music players.

## Installation

Technically possible to install via setuptools with setup.py as the settings

```bash
pip install \path\to\directory
```

Better to just download the directory and run it from there.

## Usage

Set up a virtual environment in directory and activate

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```

Install requirements

```bash
pip install -r requirements.txt
```

Enter each url in a new line in new_urls.txt, along with options. Then run the test.py script to install. Currently file paths in scripts are hard coded to my own file system.

To run from bash, give test.py and urledit.py executable priviliges

```bash
$ chmod +x test.py
$ chmod +x urledit.py
```

Add the following lines to your .bashrc

```bash
# music downloader
alias music="var=`pwd` && cd ~/downloader && ~/downloader/src/test.py && cd $var"
# url adder
adder () { read && echo -e $REPLY >> ~/downloader/new_urls.txt; }
```

Using adder will prompt you to add url and options. Using music will run test.py

```bash
$ adder
url -options
$ music
# runs test.py
```

## Support

No support. sorry :disappointed:

## Roadmap

* Write a script that allows adding songs to playlist, with iTunes Grouping (GRP1) as temp storage for most recent, and with Grouping as more permanent storage for all playlists
* Use MySQL connector to put all the metadata into a database
* Use ML to make decisions that require human intervention for now, for example:
    1. Whether lyrics match the song
    2. Proper formatting for title
    3. Proper formatting for artists

Note: The above plans may not be practical, but they are fun to learn about.

## Contributing

Would be amazed if someone would be interested in contributing. Also, project is for personal use only, so preferences are heavily tailored towards me. Forking welcome!

## Authors and acknowledgement

me.

Also my parents for getting me this far.

## License

???

## Project status

Core functionalities complete. Errors may still pop up now and then.