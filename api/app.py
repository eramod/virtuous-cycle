"""
This file contains the Application Factory and tells Python that the api
directory should be treated as a package
"""

import os

from flask import Flask
from flask_cors import CORS

# Application factory function. Any configuration, registration, and other setup
# the application needs happen inside this function. It returns the app.
def create_app(test_config=None):
  # import pdb; pdb.set_trace()
  # Create and configure the app
  app = Flask(__name__, instance_relative_config=True)

  # TODO: Point this to the deployed frontend in production.
  # Enable CORS (Cross-Origin Resource Sharing) for the app.
  CORS(app, supports_credentials=True, origins=['http://localhost:5173'])

  app.config.from_mapping(
    # Flask uses the SECRET_KEY to sign session cookies and ensure their integrity.
    SECRET_KEY='dev', # TODO: override with a random value in config.py before deploying b/c this is used by Flask and extensions to keep data safe
    DATABASE=os.path.join(app.instance_path, 'api.sqlite'),
  )

  if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path) # ensure that app.instance_path exists, because Flask will not create it automatically, but it is necessary because the project will create the SQLite DB from there
  except OSError:
    pass

  # TODO: This only serves as a reminder that the server is in fact running properly.
  # Remove once API is up and running.
  @app.route('/')
  def homepage():
    return "Virtuous Cycle Home Page"

  from . import ( db, auth, quote )
  db.init_app(app)

  app.register_blueprint(auth.bp)
  app.register_blueprint(quote.bp)

  return app