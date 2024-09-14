import yt_dlp
import json
import os, sys
from PIL import Image
import numpy as np

os.chdir('C:/Users/patri/Downloads')

import mutagen.id3 as id3

# Read txt file with urls

"""

file = open('new_urls.txt', 'r')
urls = file.read()
URLS = urls.split('\n')
file.close()

"""

URLS = ['https://www.youtube.com/watch?v=n9Ze1o_0VeA -m happy sad angry -a']

# URLS = ['https://www.youtube.com/watch?v=B5UeNLlnUOA']

# yt-dlp settings

for i in range(len(URLS)):
    INPUT = URLS[i]

    options = INPUT.split(' ')

    URL = options[0]


    ydl_opts = {
        'updatetime': False,
        'format': 'bestaudio',
        'paths': {'home': 'C:/Users/patri/Downloads'},
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': 0}
            # ,{'key': 'FFmpegMetadata'}
            # ,{'key': 'EmbedThumbnail'}
            ],
            'outtmpl': {'default': "music.%(ext)s",
                        'thumbnail': "thumbnail.%(ext)s",
                        'infojson': "data.%(ext)s"},
            'writethumbnail': True,
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

    # print(x)

    # Obtain relevant json data

    cat = data.get('categories')
    name = data.get('title')
    artists = data.get('artists')
    url = data.get('webpage_url')
    description = data.get('description')
    album = data.get('album')
    upload_date = data.get('upload_date')

    # Clean up data

    if artists == None:
        artists = data.get('uploader')

    def dupe_remove(x):
        return list(dict.fromkeys(x))

    dupe_artists = dupe_remove(artists)

    # Youtube search to find missing tags

    # Add and remove metadata to mp3 file

    tags = id3.ID3("music.mp3")

    art = artists.copy()
    art = '; '.join(art)
    print(art)

    tags.add(id3.TPE1(encoding=3, text=art))
    tags.add(id3.TPE2(encoding=3, text=f"{artists[0]}"))
    tags.add(id3.COMM(encoding=3, text=f'{url}'))
    tags.add(id3.TXXX(encoding=3, text=f'{description}'))
    tags.add(id3.TIT2(encoding=3, text=f'{name}'))
    tags.add(id3.TALB(encoding=3, text=f'{album}'))
    tags.add(id3.TDRC(encoding=3, text=f'{upload_date}'))


    if dupe_artists != artists:
        dupe_artists = ','.join(dupe_artists)
        tags.add(id3.TPE1(encoding=3, text=f'{dupe_artists}'))

    # Add thumbnail to mp3, cropping the sides if music thumbnail is square

    hor_1 = np.random.randint(0,280, 10)
    hor_2 = np.random.randint(1000, 1280, 10)

    hor = np.concatenate((hor_1, hor_2))

    ver = np.random.randint(0,720,20)

    # trying making it so you can access this image using a url
    im = Image.open("thumbnail.webp")

    pix = im.load()

    r = np.array([])
    g = np.array([])
    b = np.array([])

    for i in range(len(hor)):
        for j in range(len(ver)):
            c = np.array(pix[i,j])
            r = np.append(r, c[0])
            g= np.append(g, c[1])
            b = np.append(b, c[2])

    if np.max(r) - np.min(r) < 5 and np.max(g) - np.min(g) < 5 and np.max(b) - np.min(b) < 5:
        box = (280, 0, 1000, 720)
        region = im.crop(box)
        region.save("thumbnail.png")
    else:
        im.save("thumbnail.png")

    with open('thumbnail.png', 'rb') as albumart:
        tags.add(id3.APIC(
            encoding=3,
            mime='image/jpeg',
            type=3, desc=u'Cover',
            data=albumart.read()
        ))

    # process options

    for i in range(1, len(options)):
        if options[i][0] == '-':
            if options[i][1] == 'm':
                moodlist = list()
                counter = i + 1
                while options[counter][0] != '-':
                    moodlist.append(options[counter])
                    print(moodlist)
                    counter += 1
                tags.add(id3.TMOO(encoding=3, text = moodlist))
            if options[i][1] == 'a':
                pass
            if options[i][1] == 'g':
                pass
            if options[i][1] == 'b':
                pass
        else:
            pass

    print(tags.pprint())

    tags.save()

    # Rename the mp3 file
    # Need to add error fixing for banned characters

    try:
        os.rename('music.mp3', f'{name}.mp3')
    except FileExistsError:
        os.remove(f'{name}.mp3')
        os.rename('music.mp3', f'{name}.mp3')
