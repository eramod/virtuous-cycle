import functools

from flask import (
  Blueprint, abort, g, json, jsonify, make_response, redirect, request, session, url_for
)

from api.models import User

"""
NOTE: werkzeug implements WSGI, the standard Python interface between
applications and servers
"""
from werkzeug.security import check_password_hash, generate_password_hash
from api.app import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
  data = request.get_json()

  # Validate required fields
  required_fields = ["email", "first_name", "last_name", "phone_number", "password", "confirm_password"]
  missing_fields = [field for field in required_fields if not data.get(field)]

  if missing_fields:
    return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

  # Validate that passwords match
  if data["password"] != data["confirm_password"]:
    return jsonify({'error': 'Passwords must match.'}), 400

  # Check if user already exists
  existing_user = db.session.query(User).filter_by(email=data["email"]).first()

  if existing_user:
    return jsonify({'error': 'User already registered.'}), 400

  # Create new user
  new_user = User(
    email=data["email"],
    first_name=data["first_name"],
    last_name=data["last_name"],
    phone_number=data["phone_number"],
    password_hash=generate_password_hash(data["password"], method="pbkdf2:sha256"), # Hashes passwords securely. TODO: Use bcrypt instead?
  )

  # Save user to database
  db.session.add(new_user)
  db.session.commit()

  return jsonify({'message': 'User successfully created'}), 201

@bp.route('/login', methods=['POST', 'GET'])
def login():
  email=request.form["email"]
  password=request.form["password"]

  if not email:
    return jsonify({'message': 'Email is required'}), 400 # Bad Request
  elif not password:
    return jsonify({'message': 'Password is required'}), 400

  user = db.session.execute(
    db.select(
      User
    ).where(
      User.email == email
    )
  ).scalar_one_or_none() # Replaced `first` because it returns a tuple

  if user is None:
    return jsonify({'message': 'User not found'}), 401 # Unauthorized

  if not check_password_hash(user.password_hash, password):
    return jsonify({'message': 'Password is incorrect'}), 401

  session.clear()
  session['user_id'] = user['id']

  return make_response(jsonify({'message': 'Login successful'}), 200)

# This `@bp.before_app_request` decorator registers a function that runs before
# the view function, no matter what URL is requested in this blueprint
@bp.before_app_request
def load_logged_in_user():
  #Load logged in user from the database if they exist
  user_id = session.get('user_id')

  if user_id is None:
    g.user = None
  else:
    g.user = db.session.get(User, user_id)

@bp.route('/logout', methods=['POST'])
def logout():
  session.clear()
  g.pop('user', None)
  return make_response(jsonify({'message': 'User logged out'}), 204)

@bp.route('/user', methods=['GET'])
def user():
  user_id = session.get('user_id')

  # If there's no user_id in the session, return a 401 Unauthorized response.
  if not user_id:
    return jsonify({'error': 'Unauthorized. User must be logged in to access this endpoint.'}), 401

  db_user = db.session.get(User, user_id)

  if db_user is None:
    return jsonify({'message': 'User not found'}), 404

  user_data = {
    'id': db_user.id,
    'email': db_user.email,
    'first_name': db_user.first_name,
    'last_name': db_user.last_name,
    'phone_number': db_user.phone_number
  }

  return jsonify({'user': user_data}), 200


# Decorator for routes that require authentication
def login_required(view):
  # This decorator returns a new view function that wraps the original view it’s
  # applied to.
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.get('user') is None:
      user_id = session.get('user_id')
      if user_id:
        g.user = db.session.get(User, user_id)
    if g.user is None:
      return jsonify({'error': 'Unauthorized. User must be logged in to access this endpoint.'}), 401

    return view(**kwargs)
  return wrapped_view


# NOTE: request and session are special flask objects. It is not Pythonic to
# have a globally available object like request or session.
