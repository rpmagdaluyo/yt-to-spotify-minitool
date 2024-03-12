import json
import os
from base64 import b64encode
import six
import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth

spotify_client_id = "2f3d672957d34b17ba218fa9359c9936"
spotify_client_secret = "8591f2c4217445fc9c372fcf52b3135a"
spotify_redirect_uri = "http://localhost:3000"
scope = "playlist-modify-public, playlist-modify-private, user-library-read"
username = "richardarc18"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri=spotify_redirect_uri, scope=scope))

playlist_name = "(여자)아이들 ((G)I-DLE) Killing Voice (Vol. 2)"

def create_playlist(playlist_name):
    sp.user_playlist_create(user=username,
                        name=playlist_name,
                        public=True,
                        description="")

#print(sp._auth_headers())

#create_playlist(playlist_name)

all_playlists = sp.user_playlists(user=username)
new_playlist_id = all_playlists["items"][0]["id"]

print(new_playlist_id)
#print(sp._auth_headers())

_authorization, _bearer = list(sp._auth_headers().items())[0]

playlist_url = "https://api.spotify.com/v1/playlists/" + new_playlist_id + "/images"
image_path = r'C:\Users\ichR PC-2022\Desktop\YT to Spotify Tool\thumbnails\gidle.jpeg'
with open(image_path, "rb") as image_file:
    new_playlist_cover_b64 = b64encode(image_file.read()).decode("utf-8")

"""
TODO: Try refreshing the access token before using the playlist_upload_cover_image() method.
"""
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri=spotify_redirect_uri, scope=scope))

print(sp.playlist_upload_cover_image(playlist_id="0DpU9vCfdvLNpeTCCJdRwI", image_b64=new_playlist_cover_b64))