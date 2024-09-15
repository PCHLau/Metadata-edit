import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
client_id = 'cefb1c277b384330a56f07076383749a'
client_secret = '248407b3ddd64ef39b6cb6aa0608b155'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

name = "coldplay" #chosen artist

def spot(track, artist):
    result = sp.search(q=f'track:{track} artist:{artist}', limit=1, type='track') #search query
    albumid = result['tracks']['items'][0]['album']['id']

    alb_data = sp.albums([albumid])

    alb_genres = alb_data['albums'][0]['genres']

    artists = result['tracks']['items'][0]['artists']

    artistids = list()

    for i in artists:
        artistids.append(i['id'])

    artists_data = sp.artists(artistids)

    art_genres = []

    for artist in artists_data["artists"]:
        art_genres += artist["genres"]

    genres = [x for x in alb_genres if x in art_genres]

    if not genres:
        genres = list(set(art_genres)) + list(set(alb_genres))

    return genres