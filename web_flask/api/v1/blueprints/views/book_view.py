"""An implementation of Google book API."""
from webbrowser import get
from googleapiclient.discovery import build
from flask import render_template, request
from .. import book_api
import os
import uuid

@book_api.route('/book', methods=['GET', 'POST'], strict_slashes=False)
def book_search():
    """Uses Google api to search for books."""
    api_key = os.getenv('book_api')
    try:
        search_query = request.args.get('search_query', '')
        book_service = build('books', 'v1', developerKey=api_key)
        search_request = book_service.volumes().list(
                q=f'{search_query} in computer, software development,\
                web development, technology, programming, computer science',
                orderBy='relevance', printType='ALL',
                maxResults=10
                )
        result = search_request.execute()
        size =  len(result.get('items', []))
        books = {}
        data = result.get('items', [])
        for item in range(0, size):
            book_id = data[item].get('id', '')
            book_title = data[item].get('volumeInfo', {}).get('title' '')
            #  authors is a list converted it string
            authors = data[item].get('volumeInfo', {}).get('authors', [])
            book_authors = ' '.join(authors)
            publisher = data[item].get('volumeInfo', {}).get('publisher', '')
            description = data[item].get('volumeInfo', {}).get('description', '')
            thumbnail = data[item].get('volumeInfo', {}).get('imageLinks', {}).get('smallThumbnail', '')
            preview_link = data[item].get('volumeInfo', {}).get('previewLink', '')
            book = {
                'id': book_id, 'title': book_title, 'authors': book_authors,
                'publisher': publisher, 'description': description,
                'thumbnail': thumbnail, 'preview': preview_link
                }
            key = f'book{item}'
            books[key] = book
            version = str(uuid.uuid4())
        return render_template('book.html', books=books, version=version)
    except Exception as e:
        print('An error occured', e)
    finally:
        book_service.close()
