from flask import Flask
import os
from config import basedir, UPLOAD_FOLDER

app = Flask(__name__)

app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True

from app import views

def create_app():
    app = Flask(__name__)

    app.config.from_object('config')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    from . import views

    return app