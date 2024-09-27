#! ./.venv/bin/python3
import json
import os
import shutil

import yt_dlp  # type: ignore
from ytmusicapi import exceptions  # type: ignore
from mutagen import id3

from spotipytest import spot
from ytmusictest import ytmus
from japtest import synced, unsynced
from syncedlyricstest import synlyr
from imagetest import cropper



"""
To do:

Some sophisticated algorithm for avoiding weird artist formats (in Hoyoverse songs)

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
    file = open('new_urls.txt', 'r', encoding='utf-8')
    urls = file.read()
    urllist = urls.split('\n')
    file.close()

    # for every url (each line)
    for i, entry in enumerate(urllist):
        # ignore empty lines
        if entry == '':
            continue

        # separate urls and options
        # entry = urllist[i]
        options = entry.split(' ')
        current_url = options[0]

        # yt-dlp settings
        ydl_opts = {
            'updatetime': False,  # use time of download as time
            'format': 'bestaudio',  # best audio before encoding
            'postprocessors': [
                {  # Extract audio using ffmpeg
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': 0,
                }  # best encoding quality
            ],
            'outtmpl': {'default': "music.%(ext)s", 'infojson': "data.%(ext)s"},
            'writeinfojson': True,
        }

        # Download starts
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(current_url)

        # Open and read the JSON file
        with open('data.info.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Show keys
        # x = data.keys()

        # Obtain relevant json data
        # cat = data.get('categories')
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
        if artists is None:
            artists = [data.get('uploader')]

        # remove duplicate artist
        def dupe_remove(x):
            return list(dict.fromkeys(x))

        artists = dupe_remove(artists)

        # remove everything after ft. or feat. in title
        if 'ft.' in name:
            name = name.split('ft.')[0]
        if 'feat.' in name:
            name = name.split('feat.')[0]
        # remove empty spaces at the end of title
        name = name.rstrip()

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

        im_size = cropper(thumburl)
        im_size = f'{im_size[0]}x{im_size[1]}'

        try:
            with open('thumbnail.png', 'rb') as albumart:
                tags.add(
                    id3.APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,
                        desc=f'{thumburl}',
                        data=albumart.read(),
                    )
                )
        except FileNotFoundError:
            pass

        # process options

        jap = False
        lyr_src = ''
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
                    tags.add(id3.TMOO(encoding=3, text=moodlist))
                # add music source (anime, video game, movie, etc.)
                if options[i][1] == 's':
                    source = list()
                    counter = i + 1
                    while options[counter][0] != '-':
                        source.append(options[counter])
                        counter += 1
                    source = ' '.join(source)
                    tags.add(id3.TMED(encoding=3, text=source))
                # translate lyrics to japanese
                if options[i][1] == 'j':
                    jap = True
                # give user option to choose lyrics source
                if options[i][1] == 'l':
                    if options[i+1] == 'l':
                        lyr_src = 'lrclib'
                    elif options[i+1] == 'm':
                        lyr_src = 'musixmatch'
                    elif options[i+1] == 'n':
                        lyr_src = 'netease'
                    else:
                        pass
            else:
                pass

        # import genres and track number from spotify

        try:
            spots = spot(name, artists[0])
            genres = spots[0]
            track_number = str(spots[1])
            tags.add(id3.TCON(encoding=3, text=genres))
            tags.add(id3.TRCK(encoding=3, text=track_number))
        except IndexError: # for when spotipy search returns nothing
            print(f'''IndexError: Spotipy returned nothing for track: {name},
                  artist: {artists[0]}, in line {i}''')

        # import lyrics

        slyrics, lyrics, lyrics_source = synlyr(name, artists[0], lyr_src)

        tags.add(id3.TENC(encoding=3, text=lyrics_source))

        # translate to japanese if necessary
        if jap:
            language = 'jpn'
            try:
                tags.add(id3.USLT(encoding=3, text=f'{lyrics}', lang='jpn'))
                lyrics = unsynced(lyrics)
                tags.add(
                    id3.SYLT(encoding=3, text=slyrics, format=2, type=1, lang='jpn')
                )
                slyrics = synced(slyrics)
            except TypeError:
                pass
        else:
            language = ''

        # if synlyr did not yield lyrics, then use ytmus
        # translate if necessary
        if slyrics is None and lyrics is None:
            try:
                lyrics = ytmus(name, artists[0])['lyrics']
                if jap:
                    tags.add(id3.USLT(encoding=3, text=f'{lyrics}', lang='jpn'))
                    lyrics = unsynced(lyrics)
                tags.add(id3.USLT(encoding=3, text=f'{lyrics}'))
            except exceptions.YTMusicUserError:
                pass
        # for non-syned lyrics only
        elif slyrics is None:
            tags.add(id3.USLT(encoding=3, text=f'{lyrics}'))
        else:
            tags.add(id3.SYLT(encoding=3, text=slyrics, format=2, type=1))
            tags.add(id3.USLT(encoding=3, text=f'{lyrics}'))

        tags.save()

        print(tags.pprint())

        # Rename and move the mp3 file
        shutil.move('music.mp3', f'/mnt/c/Users/patri/Downloads/{name}.mp3')
            # os.replace('music.mp3', f'/home/patrickzklau/music/{name}.mp3')
        # except PermissionError:
        #     os.remove(f'C:/Users/patri/Downloads/{name}.mp3')
        #     os.replace('music.mp3', f'/mnt/c/Users/patri/Downloads/{name}.mp3')

        # clean up files no longer needed
        os.remove('thumbnail.png')
        os.remove('data.info.json')


downloader()
