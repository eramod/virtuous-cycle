from api.app import create_app

# See https://stackoverflow.com/questions/51395936/how-to-get-flask-app-running-with-gunicorn

if __name__ == '__main__':
    create_app = create_app()
    create_app.run()
else:
    gunicorn_app = create_app()