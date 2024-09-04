import yt_dlp
import json
import os 

os.chdir('C:/Users/patri/Downloads')



URLS = ['https://www.youtube.com/watch?v=23oZbJNSd0s']

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
        'outtmpl': {'default': "%(title)s.%(ext)s",
                    'thumbnail': "%(title)s.%(ext)s",
                    'infojson': "data.%(ext)s"},
        'writethumbnail': True,
        'writeinfojson': True

}

# Download starts
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URLS)


# Open and read the JSON file
with open('data.info.json', 'r') as file:
    data = json.load(file)

x=data.keys()

print(x)

url = data.get('thumbnail')

print(url)