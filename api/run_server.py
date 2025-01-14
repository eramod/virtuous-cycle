from src import create_app

# QUESTION: Why did we create this file? Where is it being used?

if __name__ == '__main__':
    create_app = create_app()
    create_app.run()
else:
    gunicorn_app = create_app()