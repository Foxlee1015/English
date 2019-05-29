from wtforms import Form, SubmitField, TextAreaField, validators, FileField
from flask_wtf.file import FileAllowed

class AudioForm(Form):
    audio1 = TextAreaField('What audio', [validators.data_required(), validators.Length(min=1, max=20)])
    audio2 = FileField('Audio file', validators=[FileAllowed(['mp3', 'mp4', 'wma'])])
    submit = SubmitField('okay')