import yt_dlp
import json
import os 

os.chdir('C:/Users/patri/Downloads')

from mutagen.id3 import ID3



URLS = ['https://www.youtube.com/watch?v=SxlW79tDhCA', 'https://www.youtube.com/watch?v=23oZbJNSd0s']

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

    x=data.keys()

    print(x)

    url = data.get('categories')

    name = data.get('title')

    artists = data.get('artists')

    for i in range(len(artists)):


    def dupe_remove(x):
        return list(dict.fromkeys(x))

    artists = dupe_remove(artists)

    print(url)

    # Add metadata to mp3 file

    tags = id3.ID3("music.mp3")

    tags.add(id3.TPE2(encoding=3, text=f"{artists[0]}"))

    # Rename the mp3 file

    # os.rename('music.mp3', f'{name}.mp3')

    tags.save()

