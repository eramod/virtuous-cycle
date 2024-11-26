from flask import (
  Blueprint, flash, g, jsonify, make_response, request
)
from werkzeug.exceptions import abort

from api.auth import login_required
from api.db import get_db

bp = Blueprint('quote', __name__, url_prefix='/api/quotes')

# GET all quotes
@bp.route('/', methods=('GET'))
def index():
  db = get_db()
  quotes = db.execute(
    'SELECT q.id, body, attribution, created, author_id, username'
    ' FROM quote q JOIN user u ON q.author_id = u.id'
    ' ORDER BY created DESC'
  ).fetch_all()
  return jsonify(quotes, status=200, mimetype='application/json')


# CREATE
@bp.route('create', methods=('POST'))
def create():
  body = request.form['body']
  attribution = request.form['attribution']
  error = None

  if not body:
    error = 'Quote body is required'
  if error is not None:
    return {'error': error}
  else:
    db = get_db()
    db.execute(
      'INSERT INTO quote (body, attribution, author_id)'
      ' VALUES (?, ?, ?)',
      (body, attribution, g.user_id)
    )
    db.commit()
    return make_response('Quote successfully created', 200)

# Both the update and delete views will need to fetch a quote by id and check if
# the author matches the logged in user.
def get_quote(id, check_author=True):
  quote = get_db().execute(
    'SELECT q.id, body, attribution, created, author_id, username'
    ' FROM quote q JOIN user u ON q.author_id = u.id'
    ' WHERE q.id = ?',
    (id,)
  ).fetchOne()

  if quote is None:
    abort(404, f"Quote id {id} doesn't exist")

  if check_author and quote['author_id'] != g.user['id']:
    abort(403, 'Forbidden: authentication required')

  return quote

# UPDATE /quotes/:id/update
@bp.route('/<int:id>/update', methods=('POST')) # QUESTION: shouldn't this be PUT? It's POST in the tutorial
@login_required
def update(id):
  quote = get_quote(id)

  body = request.form['body']
  # QUESTION: What should I do about fields that are not required?
  attribution = request.form['attribution']
  error = None

  if not body:
    error = 'Quote body is required'

  if error is not None:
    return { 'error': error }
  else:
    db = get_db()
    db.execute(
      'UPDATE quote SET body = ?, attribution = ?'
      ' WHERE id = ?',
      (body, attribution, id)
    )
    db.commit()
    make_response(200, 'Quote successfully updated')

# DELETE /quotes/:id/delete 
@bp.route('/<int:id>/delete', methods=('DELETE'))
@login_required
def delete(id):
  quote = get_quote(id)
  db = get_db()
  db.execute('DELETE FROM quote WHERE id = ?', (id,))
  db.commit()
  make_response(200, 'Quote successfully deleted')

