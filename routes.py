from flask import Flask
from flask import request
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
  return "<h1>Index Page</h1>"

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route("/<name>") # angle bracket is a Flask thing that captures a value from the URL
def hello_person(name):
    return f"Hello, {escape(name)}!" # string interpolation in Python3

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route('/quote/<int:quote_id>')
def quote(quote_id):
    return {'id': quote_id, 'quote_text': 'Beauty is in the eye of the beholder, and it may be necessary from time to time to give a stupid or misinformed beholder a black eye.', 'attribution': 'Miss Piggy'}