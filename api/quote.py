from flask import (
  Blueprint, g, json, jsonify, make_response, request
)
from werkzeug.exceptions import abort
from api.app import db
from api.auth import login_required

bp = Blueprint('quote', __name__, url_prefix='/api/quotes')

# GET all quotes /quotes#index
@bp.route('/', methods=['GET'])
@login_required
def index():
  # Fetch rows from the DB and build JSON data
  rows = db.execute(
    'SELECT q.id, content, attribution, created, author_id'
    ' FROM quote q JOIN user u ON q.author_id = u.id'
    ' ORDER BY created DESC'
  ).fetchall()

  quotes = []

  for row in rows:
    data = {'id': row[0], 'content': row[1], 'attribution': row[2]}
    quotes.append(data)

  return jsonify(body=quotes, status=200, mimetype='application/json')

# CREATE a quote /api/quotes#post
@bp.route('/', methods=['POST'])
@login_required
def create():
  content = request.form['content']
  # attribution is not required. Accessing the key this way will return it if present and just not do anything otherwise.
  attribution = request.form.get('attribution')
  error = None

  if not content:
    error = 'Quote content is required'
  if error is not None:
    return {'error': error}
  else:
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
  # Nicole believes forms are dictionaries, so you can access a property with
  # get and it won't error if the property is not found.
  attribution = request.form.get('attribution')
  error = None

  if not content:
    error = 'Quote content is required'

  if error is not None:
    return { 'error': error }
  else:
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
  db.execute('DELETE FROM quote WHERE id = ?', (id,))
  db.commit()
  make_response(200, 'Quote successfully deleted')

### Utility functions

# Fetch a quote from the database by id and check if the author matches the
# logged in user.
def get_quote(id, check_author=True):
  quote = db.execute(
    'SELECT q.id, content, attribution, created, author_id'
    ' FROM quote q JOIN user u ON q.author_id = u.id'
    ' WHERE q.id = ?',
    (id,)
  ).fetchone()

  if quote is None:
    abort(404, f"Quote id {id} doesn't exist")

  if check_author and quote['author_id'] != g.user['id']:
    abort(403, 'Forbidden: authentication required')

  return quote