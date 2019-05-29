from flask import request, render_template, Blueprint
from wtforms import Form, validators
from english.verb.form import search_word_Form
from english.audio.form import AudioForm
from english.models import Get_meaning, get_verbs
from random import shuffle

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home", methods=["GET", "POST"])
def home():
    audio_form = AudioForm(request.form)
    search_form = search_word_Form(request.form)
    if request.method == "POST" and search_form.validate():
        word = search_form.word.data
        word_meaning = Get_meaning(word)
        return render_template('home.html', word_meaning=word_meaning, search_form=search_form, audio_form=audio_form)
    else:
        verbs = get_verbs()
        shuffle(verbs)
        n = len(verbs)
        return render_template('home.html', search_form=search_form, audio_form=audio_form, verbs=verbs, n=n)

