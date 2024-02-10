"""Blueprints for various apis to be implemented."""
from flask import Blueprint


youtube_api = Blueprint(
        'youtube_api', __name__, template_folder='templates', static_folder='static'
        )
book_api = Blueprint(
        'book_api', __name__, template_folder='template', static_folder='static'
        )
from .views import youtube_view
from .views import book_view
