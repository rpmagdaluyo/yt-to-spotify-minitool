import os
import requests

import re
from urllib.parse import urlparse, parse_qs

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Global vars
song_titles = list()
highest_resolution_thumbnail_url = ''

# Replace 'YOUR_API_KEY' with your actual YouTube Data API key
api_key = 'AIzaSyBzG9WpUNtzLHedggQ5J1uKJA0HJpY18nI'
video_url = 'https://youtu.be/6-h-KF3Pnzo'

# Extract video ID from the YouTube video URL
parsed_url = urlparse(video_url)
video_id = None

# Get the current working directory
current_directory = os.getcwd()

# Create a 'thumbnails' directory within the current working directory if it doesn't exist
thumbnails_dir = os.path.join(current_directory, 'thumbnails')
os.makedirs(thumbnails_dir, exist_ok=True)

# Check if the URL is in the "watch?v=" format
if 'watch' in parsed_url.path: 
    # Use regular expression to discard everything but the video ID in the YouTube video URL
    # For example, if the URL provided was https://www.youtube.com/watch?v=ABC123&feature=,
    # The string returned by re.search would match 'ABC123'
    # And
    video_id_match = re.search(r'(?<=v=)[^&#]+', video_url)
    video_id = video_id_match.group(0) if video_id_match else None
else:
    # Check if the URL is in the "youtu.be/" format
    if 'youtu.be' in parsed_url.netloc:
        video_id = parsed_url.path.lstrip('/')

if video_id:
    try:
        # Build the YouTube Data API service
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Call the videos().list method to retrieve video details
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

        print("Song Titles:")
        for title in song_titles:
            print(title)

        # Extract thumbnails from the API response
        thumbnails = video_response['items'][0]['snippet']['thumbnails']

        # Get the highest resolution thumbnail
        highest_resolution_thumbnail_url = thumbnails['maxres']['url']

        # Download and save the image
        response = requests.get(highest_resolution_thumbnail_url)
        image_path = os.path.join(thumbnails_dir, f'{video_id}_thumbnail.jpg')

        with open(image_path, 'wb') as image_file:
            image_file.write(response.content)

        print(f"Thumbnail saved to: {image_path}")

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")

else:
    print("Invalid YouTube video URL.")
