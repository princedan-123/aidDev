"""The application object."""
from flask import Flask
from api.v1.blueprints import youtube_api

app = Flask(__name__)
app.register_blueprint(youtube_api)
app.run(host="localhost", port=5000, debug=True)
