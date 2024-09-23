import yt_dlp # type: ignore
import json
import os, sys
from PIL import Image
import numpy as np

import requests

from spotipytest import spot
from ytmusictest import ytmus
from japtest import synced, unsynced
from syncedlyricstest import synlyr
from imagetest import cropper
from ytmusicapi import exceptions # type: ignore

import mutagen.id3 as id3


"""
To do:

Some sophisticated algorithm for avoiding weird artist formats (in Hoyoverse songs) (next to impossible)

Empty new_urls.txt after use and send to urls.txt

SQL

Multiple album artists for album should count as a single album

Might have to reconsider file naming for songs that have the same name but different artist

"""

# Read txt file with urls

def downloader():
    """Downloads and tags songs from youtube

    Returns
    -------
    None

    """

    # initialise download settings from txt file
    file = open('new_urls.txt', 'r')
    urls = file.read()
    URLS = urls.split('\n')
    file.close()

    # for every url (each line)
    for i in range(len(URLS)):
        # separate urls and options
        INPUT = URLS[i]
        options = INPUT.split(' ')
        URL = options[0]

        # yt-dlp settings
        ydl_opts = {
            'updatetime': False, # use time of download as time
            'format': 'bestaudio', # best audio before encoding
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3', 
                'preferredquality': 0} # best encoding quality
                ],
                'outtmpl': {'default': "music.%(ext)s",
                            'infojson': "data.%(ext)s"},
                'writeinfojson': True

        }

        # Download starts
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(URL)


        # Open and read the JSON file
        with open('data.info.json', 'r', encoding='utf-8') as file:
            data = json.load(file)


        # Show keys
        x=data.keys()

        # Obtain relevant json data
        cat = data.get('categories')
        name = data.get('title')
        artists = data.get('artists')
        url = data.get('webpage_url')
        description = data.get('description')
        album = data.get('album')
        release_year = data.get('release_year')
        thumburl = data.get('thumbnail')

        # Clean up data
        
        # Use uploader if artist tag is empty
        # Mostly used for non-music category videos
        if artists == None:
            artists = [data.get('uploader')]

        # remove duplicate artist
        def dupe_remove(x):
            return list(dict.fromkeys(x))
        artists = dupe_remove(artists)

        # remove illegal windows file name characters in title
        illegal = ['/', '<', '>', ':', '"', '\\', '|', '?', '*']
        for i in illegal:
            name = name.replace(i, '')

        # initialise tag editor
        tags = id3.ID3("music.mp3")

        # Artist formatting
        art = artists.copy()
        art = '; '.join(art)

        # Add metadata
        tags.add(id3.TPE1(encoding=3, text=art))
        tags.add(id3.TPE2(encoding=3, text=f"{artists[0]}"))
        tags.add(id3.COMM(encoding=3, text=f'{url}'))
        tags.add(id3.TXXX(encoding=3, text=f'{description}'))
        tags.add(id3.TIT2(encoding=3, text=f'{name}'))
        tags.add(id3.TALB(encoding=3, text=f'{album}'))
        tags.add(id3.TDRC(encoding=3, text=f'{release_year}'))

        # Add thumbnail to mp3, cropping the sides if music thumbnail is square

        cropper(thumburl)

        with open('thumbnail.png', 'rb') as albumart:
            tags.add(id3.APIC(
                encoding=3,
                mime='image/jpeg',
                type=3, desc=f'{thumburl}',
                data=albumart.read()
            ))

        # process options

        jap = False
        for i in range(1, len(options)):
            # options all have '-' as first character
            if options[i][0] == '-':
                # add moods
                if options[i][1] == 'm':
                    moodlist = list()
                    counter = i + 1
                    while options[counter][0] != '-':
                        options[counter] = options[counter].title()
                        moodlist.append(options[counter])
                        counter += 1
                    moodlist = '; '.join(moodlist)
                    tags.add(id3.TMOO(encoding=3, text = moodlist))
                # add music source (anime, video game, movie, etc.)
                if options[i][1] == 's':
                    source = list()
                    counter = i + 1
                    while options[counter][0] != '-':
                        source.append(options[counter])
                        counter += 1
                    source = ' '.join(source)
                    tags.add(id3.TIT1(encoding=3, text = source))
                # translate lyrics to japanese
                if options[i][1] == 'j':
                    jap = True
                # nothing assigned yet
                if options[i][1] == 'b':
                    pass
            else:
                pass

        # import genres and track number from spotify

        spots = spot(name, artists[0])
        genres = spots[0]
        track_number = str(spots[1])
        tags.add(id3.TCON(encoding=3, text = genres))
        tags.add(id3.TRCK(encoding=3, text = track_number))    


        # import lyrics

        slyrics, lyrics = synlyr(name, artists[0])

        # translate to japanese if necessary
        if jap == True:
            try:
                tags.add(id3.USLT(encoding=3, text = f'{lyrics}', lang = 'jpn'))
                lyrics = unsynced(lyrics)
                tags.add(id3.SYLT(encoding=3, text = slyrics, format=2, type=1, lang = 'jpn'))
                slyrics = synced(slyrics)
            except TypeError:
                pass
        
        # if synlyr did not yield lyrics, then use ytmus
        # translate if necessary
        if slyrics == None and lyrics == None:
            try:
                lyrics = ytmus(name, artists[0])['lyrics']
                if jap == True:
                    tags.add(id3.USLT(encoding=3, text = f'{lyrics}', lang = 'jpn'))
                    lyrics = unsynced(lyrics)
                tags.add(id3.USLT(encoding=3, text = f'{lyrics}'))
            except exceptions.YTMusicUserError:
                pass
        # for non-syned lyrics only
        elif slyrics == None:
            tags.add(id3.USLT(encoding=3, text = f'{lyrics}'))
        else:
            tags.add(id3.SYLT(encoding=3, text = slyrics, format=2, type=1))
            tags.add(id3.USLT(encoding=3, text = f'{lyrics}'))

        tags.save()

        # print(tags.pprint())

        # Rename and move the mp3 file
        try:
            os.replace('music.mp3', f'C:/Users/patri/Downloads/{name}.mp3')
        except PermissionError:
            os.remove(f'C:/Users/patri/Downloads/{name}.mp3')
            os.replace('music.mp3', f'C:/Users/patri/Downloads/{name}.mp3')

        # clean up files no longer needed
        os.remove('thumbnail.png')
        os.remove('data.info.json')

downloader()