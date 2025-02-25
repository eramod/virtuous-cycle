# Virtuous Cycle

## API

### Navigate to /api folder

### Activate your virtual environment
```
pyenv activate virtuous_cycle_env
```

### Run the API server:
# Development (Not secure. Fine for local development.)
```
python3 -m flask --app api run --debug --port 5001
```
# Production
```
  gunicorn -w 4 --bind 127.0.0.1:5001 'api.run_server:gunicorn_app'
```

Heroku deployed URL: https://fierce-ocean-22944-dbcc3f05468e.herokuapp.com/

### Package Installation
Python packages listed in requirements.txt

To see all installed packages, run
  `pip3 freeze`
To add all installed packages to `requirements.txt` , run
  `pip3 freeze > requirements.txt`


### API Testing
Using `pytest`

### Debugging
Python's built-in debugger:
`import pdb; pdb.set_trace()`

Within debugger:
`n` or `next`: Execute next line
`l` or `list`: Print 5 lines before and after where you are
`c` or `continue`: Continue until you hit the next debugger
`exit`: Exit the debugger

### Deployment
Created a procfile
Using gunicorn (a WSGI server) - see https://flask.palletsprojects.com/en/stable/deploying/gunicorn/




