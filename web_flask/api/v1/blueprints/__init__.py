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
            part='snippet', maxResults=10, q='variable',
            type='video', topicId="/m/07c1v"
            )
    try:
        result = request.execute()
        size = len(result.get('items', []))
        videos = {}
        for item in range(0, size):
            video_id = result.get('items', [])[item].get('id', {}).get('videoId', None)
            video_url = f'https://youtube.com/watch?v={video_id}'
            description = result.get('items', [])[item].get('snippet', {}).get('description', None)
            title = result.get('items', [])[item].get('snippet', {}).get('title', None)
            thumbnail = result.get('items', [])[item].get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url', None)
            video = {
                'video_id':video_id, 'description':description, 'title':title,
                'thumbnail':thumbnail, 'video_url':video_url
                }
            key = f'v{item}'
            videos[key] = video
        return videos
    except Exception as e:
        print("an error occured", e)
    finally:
        youtube_client.close()
