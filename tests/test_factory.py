from api import create_app

# There’s not much to test about the factory itself.
# Most of the code will be executed for each test already, so if something fails
# the other tests will notice.

# The only behavior that can change is passing test config.
# If config is not passed, there should be some default configuration,
# otherwise the configuration should be overridden.
def test_config():
  assert not create_app().testing
  assert create_app({'TESTING': True})

# Test that the root route response data matches
# Why does it take the client fixture?
def test_root(client):
  response = client.get('/')
  assert response.data == b'Virtuous Cycle Home Page'