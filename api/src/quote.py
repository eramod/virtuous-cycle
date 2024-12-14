from flask import (
  Blueprint, g, jsonify, make_response, request
)
from werkzeug.exceptions import abort

from src.auth import login_required
from src.db import get_db
# The blueprint’s name does not modify the URL, only the endpoint.
bp = Blueprint('quote', __name__, url_prefix='/api/quotes')

# GET all quotes /quotes#index
@bp.route('/', methods=['GET'])
# @login_required
def index():
  db = get_db()
  quotes = db.execute(
    'SELECT q.id, content, attribution, created, author_id'
    ' FROM quote q JOIN user u ON q.author_id = u.id'
    ' ORDER BY created DESC'
  ).fetchall()
  return jsonify(body=quotes, status=200, mimetype='application/json') # { "quotes": quotes }

# CREATE a quote /api/quotes#post
@bp.route('/', methods=['POST'])
# @login_required
def create():
  content = request.form['content']
  # attribution is not required. Accessing the key this way will return it if present and just not do anything otherwise.
  attribution = request.form.get('attribution')
  error = None
  # QUESTION: The user is never set. Why? It's not being set because I haven't set up authentication with session cookie. No. The flask app is sending the correct response headers automatically on login, BUT the front end is not keeping the cookie around, and so it is not sending the correct request headers for subsequent requests. But why?

  if not content:
    error = 'Quote content is required'
  if error is not None:
    return {'error': error}
  else:
    db = get_db()
    db.execute(
      'INSERT INTO quote (content, attribution, author_id)'
      ' VALUES (?, ?, ?)',
      (content, attribution, g.user['id'])
    )
    db.commit()
    return make_response('Quote successfully created', 200)

# GET a single quote /quotes/:id
@bp.route('show', methods=['GET'])
@login_required
def show(id):
  quote = get_quote(id)

  return jsonify(quote, status=200, mimetype='application/json')

# UPDATE a quote /quotes/:id/update
@bp.route('/<int:id>/update', methods=['PUT'])
@login_required
def update(id):
  quote = get_quote(id)

  content = request.form['content']
  # QUESTION: What should I do about fields that are not required?
  # Nicole believes forms are dictionaries, so you can access a property with
  # get and it won't error if the property is not found.
  attribution = request.form.get('attribution')
  error = None

  if not content:
    error = 'Quote content is required'

  if error is not None:
    return { 'error': error }
  else:
    db = get_db()
    db.execute(
      'UPDATE quote SET content = ?, attribution = ?'
      ' WHERE id = ?',
      (content, attribution, id)
    )
    db.commit()
    return jsonify(quote, status=200, message='Quote successfully updated', mimetype='application/json')

# DELETE /quotes/:id/delete
@bp.route('/<int:id>/delete', methods=['DELETE'])
@login_required
def delete(id):
  quote = get_quote(id)
  db = get_db()
  db.execute('DELETE FROM quote WHERE id = ?', (id,))
  db.commit()
  make_response(200, 'Quote successfully deleted')

### Utility functions

# Fetch a quote from the database by id and check if the author matches the
# logged in user.
def get_quote(id, check_author=True):
  quote = get_db().execute(
    'SELECT q.id, content, attribution, created, author_id'
    ' FROM quote q JOIN user u ON q.author_id = u.id'
    ' WHERE q.id = ?',
    (id,)
  ).fetchOne()

  if quote is None:
    abort(404, f"Quote id {id} doesn't exist")

  if check_author and quote['author_id'] != g.user['id']:
    abort(403, 'Forbidden: authentication required')

  return quote