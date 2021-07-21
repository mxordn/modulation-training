from flask import Flask
from flask_cors import CORS
from config import UPLOAD_FOLDER

app = Flask(__name__)
CORS(app)

app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True

from . import views

def create_app():
    app = Flask(__name__)

    app.config.from_object('config')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    from . import views

    return app