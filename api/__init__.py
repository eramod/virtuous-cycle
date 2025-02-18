from api.app import create_app

# QUESTION: Why are we just importing create_app here? Should it be called?
# I believe it's because Python will run this init file automatically because of the "dunder" name?
# TODO: Does this get called from gunicorn or flask? 