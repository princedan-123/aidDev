"""The application object."""
from flask import Flask, url_for
from flask import render_template
from flask import request, redirect
import secrets
from index_form import QueryForm
from api.v1.blueprints import youtube_api
from api.v1.blueprints import book_api

app = Flask(__name__)
# creating a key for CSRF
secret_key = secrets.token_urlsafe(16)
app.secret_key = secret_key
app.register_blueprint(youtube_api)
app.register_blueprint(book_api)

@app.route('/', methods=['POST', 'GET'], strict_slashes=False)
def homepage():
    """A route for the homepage."""
    form = QueryForm()
    if form.validate_on_submit():
        data = form.search.data
        content_type = form.content.data
        if content_type == 'video':
            return redirect(url_for('youtube_api.search_videos', search_query=data))
        if content_type == 'book':
            return redirect(url_for('book_api.book_search', search_query=data))
    return render_template('index.html', form=form)

@app.route('/guide', strict_slashes=False)
def guide():
    """A route for guide template which describes how to use
        the project.
    """
    return render_template('guide.html')

@app.route('/authors', strict_slashes=False)
def authors():
    """A route for authors template which gives info about the
        authors of the project.
    """
    return render_template('authors.html')

@app.route('/story', strict_slashes=False)
def story():
    """A route for the story template."""
    return render_template('story.html')

app.run(host="localhost", port=5000, debug=True)
