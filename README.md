# Virtuous Cycle

## API

### Navigate to /api folder

### Initialize the database:
```
flask --app src init-db
```

### Run the API server:
```
flask --app src run --debug --port 5001
```

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




