"""
This file contains the Application Factory and tells Python that the src
directory should be treated as a package
"""

import os

from flask import Flask
from flask_cors import CORS

# Application factory function. Any configuration, registration, and other setup
# the application needs happen inside this function. It returns the app.
def create_app(test_config=None):
  # Create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  # Sets the Access-Control-Allow-Origin header that indicates the browser should permit loading resources from localhost:5173 during development. TODO: Point this to the deployed frontend in production.
  CORS(app, origins=['http://localhost:5173'])

  app.config.from_mapping(
    SECRET_KEY='dev', # TODO: override with a random value in config.py before deploying b/c this is used by Flask and extensions to keep data safe
    DATABASE=os.path.join(app.instance_path, 'src.sqlite'),
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

  from . import db
  db.init_app(app)

  from . import auth
  app.register_blueprint(auth.bp)

  return app