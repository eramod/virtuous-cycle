import pytest
from flask import g, session # g is the global context object in Flask
from api.db import get_db

def test_register(client, app):
  # Expect that a GET request returns a status of undefined
  assert client.get('/auth/register').status_code == 405

  assert client.post('/auth/register', data={'email':'izzy@paws.com', 'first_name':'Izzy', 'last_name': 'Eramo', 'phone_number': '1111111111', 'password': 'ilovedianne', 'confirm_password': 'ilovedianne'}).status_code == 200


def test_register_validation(client, app):
  assert True == False
  # TODO: test post errors with parametrize




