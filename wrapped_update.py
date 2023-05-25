import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

df = pd.read_json('data.json')
df['minsPlayed'] = df['msPlayed']/60000
df.head()

client_id = 'client-id'
client_secret = 'client-secret'
client_credentials_manager = SpotifyClientCredentials(client_id='client_id', client_secret='client_secret')
sp=spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_artist_genre(name):
    result = sp.search(name)
    if not result["tracks"]["items"]:
        return []
    track = result['tracks']['items'][0]
    artist = sp.artist(track['artists'][0]['external_urls']['spotify'])
    return artist["genres"]

gen_list = []
for name in df['artistName']:
    gen_list.append(get_artist_genre(name))

df_genre = pd.Series(gen_list)
df_genre = pd.DataFrame(df_genre,columns=['genre'])
df_genre_expanded = df_genre.explode("genre")
df_genre_expanded.head()

df.to_csv('MySpotify.csv')
df_genre_expanded.to_csv('GenresExpanded.csv')