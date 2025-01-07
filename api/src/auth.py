import functools

from flask import (
  Blueprint, abort, g, json, jsonify, make_response, request, session
)
"""
NOTE: werkzeug implements WSGI, the standard Python interface between
applications and servers
"""
from werkzeug.security import check_password_hash, generate_password_hash
from src.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
  email = request.form['email']
  first_name = request.form['first_name']
  last_name = request.form['last_name']
  phone_number = request.form['phone_number']
  password = request.form['password']
  confirm_password = request.form['confirm_password']
  db = get_db()
  error = None

  # TODO: Use a serializer for validation / errors.
  # https://medium.com/@jesscsommer/how-to-serialize-and-validate-your-data-with-marshmallow-a815b2276a
  if not email:
    error = 'Email is required'
  elif not first_name:
    error = 'First Name is required'
  elif not last_name:
    error = 'Last Name is required'
  elif not phone_number:
    error = 'Phone number is required'
  elif not password:
    error = 'Password is required'
  elif not confirm_password:
    error = 'Confirm password is required'
  elif password != confirm_password:
    error = 'Passwords must match'

  if error is None:
    try:
      db.execute(
        "INSERT INTO user (email, first_name, last_name, phone_number, password) VALUES (?,?,?,?,?)",
        (email, first_name, last_name, phone_number, generate_password_hash(password, method="pbkdf2"))
      )
      db.commit()
    except db.IntegrityError:
      error = f"User {email} is already registered."
    else:
      return make_response('User successfully created', 200)
  else:
    return {'error': error}

@bp.route('/login', methods=['POST'])
def login():
  email = request.form['email']
  password = request.form['password']
  db = get_db()
  error = None

  if not email:
    error = 'Email is required'
  elif not password:
    error = 'Password is required'

  if error is None:
    user = db.execute(
      'SELECT * FROM user WHERE email = ?',
      (email,)
    ).fetchone()

    if user is None:
      error = 'User not found'
    elif not check_password_hash(user['password'], password):
      error = 'Password is incorrect'

    session.clear()
    session['user_id'] = user['id']

    response = make_response(jsonify({'message': 'Login successful'}), 200)
    return response

  else:
    return jsonify({'message': 'Invalid username or password'}), 401

# This `@bp.before_app_request` decorator registers a function that runs before
# the view function, no matter what URL is requested in this blueprint
@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')
  db = get_db()

  if user_id is None:
    g.user = None
  else:
    g.user = db.execute(
      'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

@bp.route('/logout', methods=['POST'])
def logout():
  session.clear()
  return make_response(jsonify('User logged out'), 204)

@bp.route('/user', methods=['GET'])
def user():
  user_id = session.get('user_id')
  db = get_db()

  db_user = db.execute(
    'SELECT * FROM user WHERE id = ?', (user_id,)
  ).fetchone()

  if db_user is None:
    return make_response(jsonify('User not found'), 404)
  else:
    user = {
      'id': db_user['id'],
      'email': db_user['email'],
      'first_name': db_user['first_name'],
      'last_name': db_user['last_name'],
      'phone_number': db_user['phone_number']
    }
    # TODO: This converts the user object to a JSON string. Do I need to do this?
    json_data = json.dumps(user)

    return jsonify(body={'user': json_data}, status=200, mimetype='application/json')


# Decorator to be used for resources that require a user to be logged in for access.
def login_required(view):
  # This decorator returns a new view function that wraps the original view it’s
  # applied to.
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return abort(401, 'Unauthorized. User must be logged in to access this endpoint.')
    return view(**kwargs)
  return wrapped_view


# NOTE: request and session are special flask objects. It is not Pythonic to
# have a globally available object like request or session.
