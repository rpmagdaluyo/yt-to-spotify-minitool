import json
import os
import base64
import six
import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth

#TODO: Add YT-side functions
""" YT Vars """
yt_title = ''
yt_description = ''
yt_song_list = []

""" YT Funcs """
def get_description(yt_url):
    return

def get_title(yt_url):
    return

def get_song_list(yt_description):
    return


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

""" Spotify Funcs """

def create_playlist(playlist_name):
    sp.user_playlist_create(user=username,
                            name=playlist_name,
                            public=True,
                            description="")

#_authorization, _bearer = list(sp._auth_headers().items())[0]

def update_playlist_cover(playlist_id, cover_image):
    sp.playlist_upload_cover_image(playlist_id=playlist_id, 
                                   image_b64=cover_image)

#TODO: Test Spotipy search and add songs
def add_songs(playlist_id, song_list):
    for song in song_list:
        #search for the song
        # add the song to the target playlist
        return

all_playlists = sp.user_playlists(user=username)
newest_playlist_id = all_playlists["items"][0]["id"]

#playlist_name = "(여자)아이들 ((G)I-DLE) Killing Voice (Vol. 2)"
playlist_name = "TEST PLAYLIST"
create_playlist(playlist_name)

newest_playlist_url = "https://api.spotify.com/v1/playlists/" + newest_playlist_id + "/images"
image_name = 'OkEDeFKRnio_thumbnail.jpg'
image_path = os.path.join(os.getcwd(), 'thumbnails', image_name)
with open(image_path, "rb") as image_file:
    new_playlist_cover_b64 = base64.b64encode(image_file.read()).decode("utf-8")

update_playlist_cover(newest_playlist_id, new_playlist_cover_b64)