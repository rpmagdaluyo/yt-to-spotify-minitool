import os
import requests

import re
from urllib.parse import urlparse, parse_qs

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

""" global vars """
#song_titles = list()
#highest_resolution_thumbnail_url = ''

def save_thumbnail(save_path, thumbnail):
    with open(save_path, 'wb') as save_file:
        save_file.write(thumbnail.content)
    print(f"Thumbnail saved to: {save_path}")

def get_video_id(video_url):
    parsed_url = urlparse(video_url)

    # Check if the URL is in the "watch?v=" format
    if 'watch' in parsed_url.path: 
        # Use regular expression to discard everything but the video ID in the YouTube video URL
        # For example, if the URL provided was https://www.youtube.com/watch?v=ABC123&feature=,
        # The string returned by re.search would match 'ABC123'
        # And
        video_id_match = re.search(r'(?<=v=)[^&#]+', video_url)
        video_id = video_id_match.group(0) if video_id_match else None
    # Check if the URL is in the "youtu.be/" format
    else:
        if 'youtu.be' in parsed_url.netloc:
            video_id = parsed_url.path.lstrip('/')

    return video_id

def get_song_list(video_id):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Call the list() method on youtube.videos() to retrieve video details
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        # Extract the video description from the API response
        video_snippet = video_response['items'][0]['snippet']
        description = video_snippet['description']

        # Use a regex to extract song titles without timestamps
        song_titles_match = re.findall(r'\d+:\d+\s*(.*)', description)
        song_titles = [title.strip() for title in song_titles_match]

        return song_titles
    
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")

def get_video_title(video_id):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Call the list() method on youtube.videos() to retrieve video details
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        # Extract the video title from the API response
        video_snippet = video_response['items'][0]['snippet']
        video_title = video_snippet['title']

        return video_title
    
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")

def get_thumbnail_url(video_id):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Call the videos().list method to retrieve video details
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        thumbnails = video_response['items'][0]['snippet']['thumbnails']

        # Get the highest resolution thumbnail
        highest_resolution_thumbnail_url = thumbnails['maxres']['url']

        return highest_resolution_thumbnail_url
    
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")

def get_artist_name(video_title):
    # Regex pattern to match text inside parentheses
    pattern_with_parentheses = r'\((.*?)\)\s*의'

    # Regex pattern to match text before '의'
    pattern_without_parentheses = r'^(.*?)의'

    # Check if there are parentheses before '의'
    match_with_parentheses = re.search(pattern_with_parentheses, video_title)
    if match_with_parentheses:
        return match_with_parentheses.group(1)  # Return text inside parentheses
    else:
        # If there are no parentheses, match text before '의'
        match_without_parentheses = re.search(pattern_without_parentheses, video_title)
        if match_without_parentheses:
            return match_without_parentheses.group(1)  # Return text before '의'
    
    # If neither pattern matches, return None
    return None        

# Get the current working directory
current_directory = os.getcwd()

# Create a 'thumbnails' directory within the current working directory if it doesn't exist
thumbnails_dir = os.path.join(current_directory, 'thumbnails')
os.makedirs(thumbnails_dir, exist_ok=True)

def download_thumbnail(thumbnail_url, filename):
    # Get the current working directory
    current_directory = os.getcwd()

    # Create a 'thumbnails' directory within the current working directory if it doesn't exist
    thumbnails_dir = os.path.join(current_directory, 'thumbnails')
    os.makedirs(thumbnails_dir, exist_ok=True)

    # Get the image file from its URL
    thumbnail = requests.get(thumbnail_url)

    image_path = os.path.join(thumbnails_dir, f'{filename}_thumbnail.jpg')
    save_thumbnail(image_path, thumbnail)

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual YouTube Data API key
    api_key = 'AIzaSyBzG9WpUNtzLHedggQ5J1uKJA0HJpY18nI'

    test_url =  'https://youtu.be/cP2q1XWBhl4'

    test_video_id = get_video_id(test_url)
    test_song_list = get_song_list(test_video_id)
    test_thumbnail_url = get_thumbnail_url(test_video_id)
    test_video_title = get_video_title(test_video_id)
    test_artist_name = get_artist_name(test_video_title)
    download_thumbnail(test_thumbnail_url, test_artist_name)
