from english.verb.form import input_sentence_Form, search_word_Form
from flask import request, render_template, Blueprint
from english.models import get_random_verb, Get_meaning, get_data

verb_b = Blueprint('verb', __name__)

@verb_b.route("/verb")
def verb_random():
    verb = get_random_verb()
    input_form = input_sentence_Form(request.form)
    search_form = search_word_Form(request.form)
    sen1, exp1, rd_sen, r_n = get_data(verb)
    meaning = Get_meaning(verb)
    return render_template('verb.html', input_form=input_form, search_form=search_form, rd_sen=rd_sen, r_n=r_n, exp1=exp1, verb=verb, sen=sen1, meaning=meaning)

@verb_b.route("/verb/<string:verb>", methods=["GET", "POST"])
def verb(verb):
    input_form = input_sentence_Form(request.form)
    search_form = search_word_Form(request.form)
    sen1, exp1, rd_sen, r_n = get_data(verb)
    meaning = Get_meaning(verb)
    if request.method == "POST" and input_form.validate():
        sentence_in = input_form.sentence_input.data
        if sen1 == sentence_in:
            flash('Correct')
            return redirect(url_for('verb_random'))
        else:
            flash('Wrong')
            return render_template('verb.html', input_form=input_form, search_form=search_form, rd_sen=rd_sen, r_n=r_n, exp1=exp1, verb=verb, sen=sen1, meaning=meaning)
    elif request.method == "POST":
        flash('Try again. (Nothing is submitted.)')
        return render_template('verb.html', input_form=input_form, search_form=search_form, rd_sen=rd_sen, r_n=r_n, exp1=exp1, verb=verb, sen=sen1, meaning=meaning)

    else:
        return render_template('verb.html', input_form=input_form, search_form=search_form, rd_sen=rd_sen, r_n=r_n, exp1=exp1, verb=verb, sen=sen1, meaning=meaning)