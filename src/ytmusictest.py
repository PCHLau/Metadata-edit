from ytmusicapi import YTMusic # type: ignore

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
    video_id = results[0]['videoId']
    result = ytmusic.get_watch_playlist(video_id, limit = 1)
    browse = result['lyrics']
    lyrics = ytmusic.get_lyrics(browse)

    return lyrics
