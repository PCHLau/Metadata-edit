from ytmusicapi import YTMusic # type: ignore
from ytmusicapi import exceptions
import json

def ytmus(track: str, artist: str) -> dict:
    """Gives song lyrics from YTMusic api  

    Parameters
    ----------
    track : str
        Song name
    artist : str
        album artist name

    Returns
    -------
    dict
        Song lyrics
    """

    # Find song of Youtube Music
    entry = track + ' ' + artist
    ytmusic = YTMusic()
    results = ytmusic.search(query = f'{entry}', filter = 'songs', limit = 1)
    # Convoluted steps to get lyrics from api
    id = results[0]['videoId']
    result = ytmusic.get_watch_playlist(id, limit = 1)
    browse = result['lyrics']
    lyrics = ytmusic.get_lyrics(browse)

    return lyrics