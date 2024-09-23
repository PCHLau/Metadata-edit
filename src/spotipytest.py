import spotipy # type: ignore
from spotipy.oauth2 import SpotifyClientCredentials # type: ignore
# To access authorised Spotify data, need client id
# Obtained for spotipy web api developer project
client_id = 'cefb1c277b384330a56f07076383749a'
client_secret = '248407b3ddd64ef39b6cb6aa0608b155'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

def spot(track: str, artist: str) -> tuple[list, int]:
    """Use spotify web api to return genre and track number

    Parameters
    ----------
    track : str
        Song name
    artist : str
        album artist name

    Returns
    -------
    tuple[list, int]
        tuple of list of album/artist genres, and track number of song
    """    
    # Search for and extract useful information
    result: dict = sp.search(q=f'track:{track} artist:{artist}', limit=1, type='track') #search query
    track_number: int = result['tracks']['items'][0]['track_number']
    albumid: str = result['tracks']['items'][0]['album']['id']
    alb_data: dict = sp.albums([albumid])
    alb_genres = alb_data['albums'][0]['genres']
    artists = result['tracks']['items'][0]['artists']

    # Find artist genres
    artistids = list()
    for i in artists:
        artistids.append(i['id'])
    artists_data: dict = sp.artists(artistids)
    art_genres: list = list()
    for i in artists_data['artists']:
        art_genres += i['genres']
    
    # Try to find intersect in artist and album genres
    genres = [x for x in alb_genres if x in art_genres]
    # If that doesn't exist, add the two lists
    if not genres:
        genres = list(set(art_genres)) + list(set(alb_genres))

    return genres, track_number