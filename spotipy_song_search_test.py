import json
import os
import base64
import six
import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth

""" Spotipy Vars """

spotify_client_id = "2f3d672957d34b17ba218fa9359c9936"
spotify_client_secret = "8591f2c4217445fc9c372fcf52b3135a"
spotify_redirect_uri = "http://localhost:3000"
scopes = "playlist-modify-public, \
          playlist-modify-private, \
          user-library-read, \
          ugc-image-upload"

username = "richardarc18"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri=spotify_redirect_uri, scope=scopes))

artist_name = 'Zion.T'
track_name = '모르는 사람'
query_string = f'track{track_name}&type=track&market=KR&limit=1'
print(json.dumps(sp.search(q=query_string,
          limit=10,
          type="track"), indent=4))
