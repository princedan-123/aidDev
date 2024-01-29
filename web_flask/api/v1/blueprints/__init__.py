"""Blueprints for various apis to be implemented."""
from flask import Blueprint
from googleapiclient.discovery import build
import os

youtube_api = Blueprint('youtube_api', __name__)

@youtube_api.route('/videos', strict_slashes=False)
def search_videos():
    api_key = os.getenv('google_api_key')
    youtube_client = build('youtube', 'v3', developerKey=api_key)
    request = youtube_client.search().list(
            part="snippet", maxResults=1, q='variable',
            type='video', topicId="/m/07c1v"
            )
    try:
        return request.execute()
    except Exception as e:
        print("an error occured", e)
    finally:
        youtube_client.close()
