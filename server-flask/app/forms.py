from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators

class UploadAndSelectActions(FlaskForm):
    klauselnP = BooleanField('Klauseln prüfen')
    aSProg = BooleanField('Aussenstimmen prüfen')
    bassPart = StringField("Bassstimme angeben (optional, bei Benutzung der Vorlagen bitte nicht ändern)", default="1", validators=[validators.DataRequired()])
