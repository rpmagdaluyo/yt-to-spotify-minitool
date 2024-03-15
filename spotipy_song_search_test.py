import json
import os
import base64
import six
import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth

""" Using Spotipy """

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
query_string = f'artist:ziont'
#print(json.dumps(sp.search(q=query_string, limit=1, type="track", market='KR'), indent=4))

""" Using requests """

# Get a token to use search endpoint
def get_token(client_id, client_secret):
    endpoint = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type' : 'client_credentials',
        'client_id' : client_id,
        'client_secret' : client_secret
    }

    response = requests.post(
        endpoint,
        data=data,
        headers=headers,
        verify=True
    )

    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))
    else:
        print('Error:', response.status_code)

    return response
    #print(response.json())


#get_token(spotify_client_id, spotify_client_secret)
    
# Search endpoint
def search(query, type, limit=10, market='US'):
    endpoint = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization' : 'Bearer BQCi7sYzwG772le84HVEp0ROFn2dY5CZMidTIm8ppO9pff70JNwCJ4Mfbtx9otb5yJv8B5CrYPAvD2G69Euq3QBxAQAPp2aerr-a-YKWWAfElSsm9Io'

    }
    params = {
        'q' : query,
        'type' : type,
        'market' : market,
        'limit' : limit
    }

    response = requests.get(
        endpoint,
        headers=headers,
        params=params,
    )

    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))
    else:
        print('Error:', response.status_code)

    return response

search('artist:헤이즈', type='track', limit=1, market='KR')

"""
url = 'https://api.spotify.com/v1/search'
params = {
    'q': 'artist:ziont',
    'type': 'track',
    'market': 'kr',
    'limit': 1
}
headers = {
    'Authorization': 'Bearer 1POdFZRZbvb...qqillRxMr2z'
}

response = requests.get(url, params=params, headers=headers)
"""
