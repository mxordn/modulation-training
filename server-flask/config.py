import os
basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = basedir + '/app/uploads/'
MODULS_FOLDER = basedir + '/app/modulationen/'
ALLOWED_EXTENSIONS = set(['xml', 'musicxml'])

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
