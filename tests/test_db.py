import sqlite3

import pytest
from api.db import get_db

# Within an application context, get_db should return the same connection each
# time it’s called.
def test_get_close_db(app):
  with app.app_context():
    db = get_db()
    assert db is get_db()

  with pytest.raises(sqlite3.ProgrammingError) as e:
    db.execute('SELECT 1')

  # After the context, the connection should be closed.
  assert 'closed' in str(e.value)

# The init-db command should call the init_db function and output a message.
# This test uses Pytest’s monkeypatch fixture to replace the init_db function
# with one that records that it’s been called.
def test_init_db_command(runner, monkeypatch):
  class Recorder(object):
    called = False

  def fake_init_db():
    Recorder.called = True

  monkeypatch.setattr('api.db.init_db', fake_init_db)
  result = runner.invoke(args=['init-db'])

  assert 'Initialized' in result.output
  assert Recorder.called