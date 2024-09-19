import yt_dlp
import json
import os, sys
from PIL import Image
import numpy as np

import requests

from spotipytest import spot
from ytmusictest import ytmus
from syncedlyricstest import synlyr
from ytmusicapi import exceptions

import mutagen.id3 as id3


"""
To do:

Some sophisticated algorithm for avoiding weird artist formats (in Hoyoverse songs)

Support for different thumbnail sizes

Change destination and execution directory

Empty new_urls.txt after use and send to urls.txt

SQL

Execute from commandline (both adding text and the script)

Maybe split into multiple files

Multiple album artists for album should count as a single album

add romaji lyrics for japanese songs

"""

# Read txt file with urls

def downloader():

    # os.chdir('C:/Users/patri/Downloads')

    print(os.getcwd())

    file = open('new_urls.txt', 'r')
    urls = file.read()
    URLS = urls.split('\n')
    file.close()


    # yt-dlp settings

    for i in range(len(URLS)):
        INPUT = URLS[i]

        options = INPUT.split(' ')

        URL = options[0]


        ydl_opts = {
            'updatetime': False,
            'format': 'bestaudio',
            # 'paths': {'home': 'C:/Users/patri/Downloads'},
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': 0}
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
        # x=data.keys()

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

        if artists == None:
            artists = [data.get('uploader')]

        # Need something more sophisticated for Hoyoverse songs
        def dupe_remove(x):
            return list(dict.fromkeys(x))

        artists = dupe_remove(artists)

        illegal = ['/', '<', '>', ':', '"', '\\', '|', '?', '*']

        for i in illegal:
            name = name.replace(i, '')

        # Youtube search to find missing tags

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

        hor_1 = np.random.randint(90,190, 10)
        hor_2 = np.random.randint(1090, 1190, 10)

        hor = np.concatenate((hor_1, hor_2))

        ver = np.random.randint(260,460,20)

        im = Image.open(requests.get(thumburl, stream=True).raw)

        pix = im.load()

        # try to add support for multiple thumbnail sizes

        if im.size == (1280, 720):
            r = np.array([])
            g = np.array([])
            b = np.array([])

            for i in range(len(hor)):
                for j in range(len(ver)):
                    c = np.array(pix[i,j])
                    r = np.append(r, c[0])
                    g= np.append(g, c[1])
                    b = np.append(b, c[2])

            if np.max(r) - np.min(r) < 10 and np.max(g) - np.min(g) < 10 and np.max(b) - np.min(b) < 10:
                box = (280, 0, 1000, 720)
                region = im.crop(box)
                region.save("thumbnail.png")
            else:
                im.save("thumbnail.png")
        else:
            im.save("thumbnail.png")

        with open('thumbnail.png', 'rb') as albumart:
            tags.add(id3.APIC(
                encoding=3,
                mime='image/jpeg',
                type=3, desc=f'{thumburl}',
                data=albumart.read()
            ))

        # process options

        for i in range(1, len(options)):
            if options[i][0] == '-':
                if options[i][1] == 'm':
                    moodlist = list()
                    counter = i + 1
                    while options[counter][0] != '-':
                        options[counter] = options[counter].title()
                        moodlist.append(options[counter])
                        counter += 1
                    moodlist = '; '.join(moodlist)
                    tags.add(id3.TMOO(encoding=3, text = moodlist))
                if options[i][1] == 's':
                    source = list()
                    counter = i + 1
                    while options[counter][0] != '-':
                        source.append(options[counter])
                        counter += 1
                    source = ' '.join(source)
                    tags.add(id3.TIT1(encoding=3, text = source))
                if options[i][1] == 'g':
                    pass
                if options[i][1] == 'b':
                    pass
            else:
                pass

        # import genres and track number

        spots = spot(name, artists[0])

        genres = spots[0]
        track_number = str(spots[1])

        tags.add(id3.TCON(encoding=3, text = genres))
        tags.add(id3.TRCK(encoding=3, text = track_number))    


        # import lyrics

        slyrics, lyrics = synlyr(name, artists[0])

        if slyrics == None:
            try:
                lyrics = ytmus(name, artists[0])['lyrics']
                tags.add(id3.USLT(encoding=3, text = f'{lyrics}'))
            except exceptions.YTMusicUserError:
                pass
        else:
            tags.add(id3.SYLT(encoding=3, text = slyrics, format=2, type=1))
            tags.add(id3.USLT(encoding=3, text = f'{lyrics}'))


        tags.save()

        # print(tags.pprint())

        # Rename the mp3 file
        # Need to add error fixing for banned characters

        try:
            os.replace('music.mp3', f'C:/Users/patri/Downloads/{name}.mp3')
        except FileExistsError:
            os.remove(f'{name}.mp3')
            os.rename('music.mp3', f'{name}.mp3')

        os.remove('thumbnail.png')
        os.remove('data.info.json')

downloader()