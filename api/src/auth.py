import functools

from flask import (
  Blueprint, flash, g, make_response, redirect, request, session, url_for
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
        (email, first_name, last_name, phone_number, generate_password_hash(password))
      )
      db.commit()
    except db.IntegrityError:
      error = f"User {email} is already registered."
    else:
      # What should the backend do after it saves something to the DB?
      # It should send a response that it worked
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

    if error is None:
      session.clear()
      session['user_id'] = user['id']
      return {'user_id': user['id']}
    else:
      return {'error': error}

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return make_response('User logged out', 200)



# NOTE: request and session are special flask objects. It is not Pythonic to have a globally available object like request or session.
