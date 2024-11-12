import functools

from flask import (
  Blueprint, flash, g, redirect, request, session, url_for
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
  username = request.form['username']
  password = request.form['password']
  confirm_password = request.form['confirm_password']
  db = get_db()
  error = None

  if not username:
    error = 'Username is required'
  elif not password:
    error = 'Password is required'
  elif not confirm_password:
    error = 'Confirm password is required'
  elif password != confirm_password:
    error = 'Passwords must match'

  if error is None:
    try:
      db.execute(
        "INSERT INTO user (username, password) VALUES (?,?)",
        (username, generate_password_hash(password))
      )
      db.commit()
    except db.IntegrityError:
      error = f"User {username} is already registered."
    else:
      return redirect(url_for("auth.login"))
  else:
    return {'error': error}

@bp.route('/login', methods=['POST'])
def login():
  username = request.form['username']
  password = request.form['password']
  db = get_db()
  error = None

  if not username:
    error = 'Username is required'
  elif not password:
    error = 'Password is required'

  if error is None:
    user = db.execute(
      'SELECT * FROM user WHERE username = ?',
      (username,)
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



# NOTE: request and session are special flask objects. It is not Pythonic to have a globally available object like request or session.
