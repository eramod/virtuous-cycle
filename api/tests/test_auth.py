import pytest
from flask import g, session # g is the global context object in Flask
from src.db import get_db

def test_register(client, app):
  assert client.get('/auth/register').status_code == 200

