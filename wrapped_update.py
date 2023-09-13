import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth

df = pd.read_json('data.json')
df['minsPlayed'] = df['msPlayed']/60000
df.head()

#spotipy environment variables
SPOTIPY_CLIENT_ID = 'ee169470215f42c193d160758e86b089'
SPOTIPY_CLIENT_SECRET = 'b969ad21717c4e2c983a6c24fbd868f6'
SPOTIPY_REDIRECT_URI = 'ee169470215f42c193d160758e86b089'
SCOPE = 'user-top-read'

brock = 'https://open.spotify.com/artist/1Bl6wpkWCQ4KVgnASpvzzA?si=uVD1RiroR4K3EZ4GetXWEA'

#client_credentials_manager = SpotifyClientCredentials(client_id='ee169470215f42c193d160758e86b089', client_secret='b969ad21717c4e2c983a6c24fbd868f6')
sp=spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, 
                                              client_secret=SPOTIPY_CLIENT_SECRET,
                                             redirect_uri=SPOTIPY_REDIRECT_URI,
                                             scope=SCOPE))

def get_artist_genre(name):
    result = sp.search(name, limit=1, type=artist)
    if not result["tracks"]["items"]:
        return []
    track = result['tracks']['items'][0]
    artist = result['artists']
    album = sp.album(track['artists'][0]['external_urls']['spotify'])
    print(artist['items'][0]["genres"])
    print("artist genres: ", artist['genres'])
    print("album genres: ", album['genres'])
    return artist["genres"]

def get_artist_genre2(name):
    result = sp.search(name, limit = 1, type = 'artist')
    artists = result['artists']
    print(artists['items'][0]['genres'])

#Will return the album of a given song
#Parameters: name: the song name
def get_album(name):
    result = sp.search(name)
    if not result["tracks"]["items"]:
        return []
    track = result['tracks']['items'][0]
    artist = sp.artist(track['artists'][0]['external_urls']['spotify'])
    return artist['albums']

def old():
    gen_list = []
    for name in df['artistName']:
        gen_list.append(get_artist_genre('brockhampton'))

    df_genre = pd.Series(gen_list)
    df_genre = pd.DataFrame(df_genre,columns=['genre'])
    df_genre_expanded = df_genre.explode("genre")
    df_genre_expanded.head()

    df.to_csv('MySpotify.csv')
    df_genre_expanded.to_csv('GenresExpanded.csv')

def main():
    get_artist_genre2("brockhampton")
    old()