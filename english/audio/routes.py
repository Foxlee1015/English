from flask import Blueprint, render_template, request
from english.audio.form import AudioForm
from werkzeug.utils import secure_filename

audio_b = Blueprint('audio', __name__)

@audio_b.route("/audio/register", methods=["GET", "POST"])
def audio():
    audio_form = AudioForm(request.form)
    if request.method == "POST" and audio_form.validate():
        file = request.files['file']  # post 된 파일 정보 가져옴
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('audio.html', audio_form=audio_form)
    else:
        return render_template('audio.html', audio_form=audio_form)

@audio_b.route("/audio/list", methods=["GET", "POST"])
def audio_list():
    return render_template('audio_list.html')