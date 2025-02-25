import os
import tempfile

import pytest
from api import create_app
from api.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
  _data_sql = f.read().decode('utf8')

'''
The app fixture will call the factory and pass test_config to configure the
application and database for testing instead of using your local development
configuration.
'''
@pytest.fixture
def app():
  # tempfile.mkstemp creates and opens a temporary file, returning the file descriptor and the path to it
  db_fd, db_path = tempfile.mkstemp() # this is destructuring

  app = create_app({
    'TESTING': True,
    'DATABASE': db_path,
  })

  # with statement is called a context manager. Will return things to the clean state, regardless of whether the function failed or succeeded. This with is referring to the app context, and this is what gets cleaned up.
  with app.app_context():
    init_db()
    # TODO: Update to use SQL Alchemy
    # get_db().executescript(_data_sql)

    yield app # QUESTION: What does this `yield` do? Does it identify this function as a generator?
    # Generators are memory-efficient because they only load the data needed to
    # process the next value in the iterable. This allows them to perform
    # operations on otherwise prohibitively large value ranges.

    os.close(db_fd)
    os.unlink(db_path)

# Good reasons to use pytest.
# 1. Fixtures allow you to define functions or objects in this config file, pass them to your unit test functions, and pytest will know how to find them.
# 2. it allows you to pass multiple inputs for test functions without writing the same test multiple times through parametrize https://docs.pytest.org/en/stable/how-to/parametrize.html

# Tests will use the client fixture to make requests to the application without
# running the server.
@pytest.fixture
def client(app):
  return app.test_client()

# This runner fixture creates a runner that can call the Click commands
# registered with the application.
# TODO: I don't need to click around, so this seems like an unnecessary fixture.
@pytest.fixture
def runner(app):
  return app.test_cli_runner()


# For most of the views, a user needs to be logged in. The easiest way to do
# this in tests is to make a POST request to the login view with the client.
# Rather than writing that out every time, you can write a class with methods
# to do that, and use a fixture to pass it the client for each test.
class AuthActions(object):
  def __init__(self, client):
      self._client = client

  def login(self, username='test', password='test'):
      return self._client.post(
          '/auth/login',
          data={'username': username, 'password': password}
      )

  def logout(self):
      return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
  return AuthActions(client)
