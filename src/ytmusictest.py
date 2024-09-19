from ytmusicapi import YTMusic
from ytmusicapi import exceptions
import json

def ytmus(track, artist):

    entry = track + ' ' + artist

    ytmusic = YTMusic()

    results = ytmusic.search(query = f'{entry}', filter = 'songs', limit = 1)

    id = results[0]['videoId']

    result = ytmusic.get_watch_playlist(id, limit = 1)

    browse = result['lyrics']

    lyrics = ytmusic.get_lyrics(browse)

    return lyrics