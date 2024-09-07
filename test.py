import yt_dlp
import json
import os 

os.chdir('C:/Users/patri/Downloads')

import mutagen.id3 as id3

# Read txt file with urls

file = open('new_urls.txt', 'r')
urls = file.read()
URLS = urls.split('\n')
file.close()

# yt-dlp settings

for i in range(len(URLS)):
    URL = [URLS[i]]

    ydl_opts = {
        'updatetime': False,
        'format': 'bestaudio',
        'paths': {'home': 'C:/Users/patri/Downloads'},
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': 0},
            {'key': 'FFmpegMetadata'}
            # {'key': 'EmbedThumbnail'}
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

    print(x)

    # Obtain relevant json data

    cat = data.get('categories')
    name = data.get('title')
    artists = data.get('artists')
    url = data.get('webpage_url')
    description = data.get('description')

    tag = data.get('tags')

    print(tag)

    # Clean up data

    

    if artists == None:
        artists = data.get('uploader')

    def dupe_remove(x):
        return list(dict.fromkeys(x))

    dupe_artists = dupe_remove(artists)

    # Youtube search to find missing tags

    # Add and remove metadata to mp3 file

    tags = id3.ID3("music.mp3")

    tags.delall('TXXX')
    tags.delall('COMM')

    tags.add(id3.TPE2(encoding=3, text=f"{artists[0]}"))
    tags.add(id3.COMM(encoding=3, text=f'{url}'))
    tags.add(id3.TXXX(encoding=3, text=f'{description}'))

    if dupe_artists != artists:
        dupe_artists = ','.join(dupe_artists)
        tags.add(id3.TPE1(encoding=3, text=f'{dupe_artists}'))

    
    tags.save()

    print(tags.pprint())

    # Rename the mp3 file
    # Need to add error fixing for banned characters

    try:
        os.rename('music.mp3', f'{name}.mp3')
    except FileExistsError:
        os.remove(f'{name}.mp3')
        os.rename('music.mp3', f'{name}.mp3')
        

