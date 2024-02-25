"""Implementation of youtube api view."""
from .. import youtube_api
from flask import request
from googleapiclient.discovery import build
from flask import render_template
import uuid
import os

@youtube_api.route('/videos', methods=['GET'], strict_slashes=False)
def search_videos():
    query = request.args.get('search_query')
    api_key = os.getenv('google_api_key_two')
    youtube_client = build('youtube', 'v3', developerKey=api_key)
    client_request = youtube_client.search().list(
            part='snippet', maxResults=10, q=f'{query}',
            type='video', topicId="/m/07c1v"
            )
    try:
        result = client_request.execute()
        size = len(result.get('items', []))
        videos = {}
        for item in range(0, size):
            video_id = result.get('items', [])[item].get('id', {}).get('videoId', '')
            video_url = f'https://youtube.com/watch?v={video_id}'
            description = result.get('items', [])[item].get('snippet', {}).get('description', '')
            title = result.get('items', [])[item].get('snippet', {}).get('title', '')
            thumbnail = result.get('items', [])[item].get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url', '')
            if len(title) > 25:
                title_edit = title[0:26]
                title = f'{title_edit}...'
            video = {
                'video_id':video_id, 'description':description, 'title':title,
                'thumbnail':thumbnail, 'video_url':video_url
                }
            key = f'v{item}'
            videos[key] = video
        version = str(uuid.uuid4())
        return render_template('response.html', videos=videos, version=version, search_query=query)
    except Exception as e:
        print("an error occured", e)
    finally:
        youtube_client.close()
