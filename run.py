from flask import Flask, render_template, request, flash, url_for, redirect
from wtforms import Form, SubmitField, TextAreaField, validators
import random, json
from random import shuffle

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

class input_sentent_Form(Form):
    sentence_input = TextAreaField('input', [validators.Length(min=1, max=100)])
    submit = SubmitField('문장 제출')

def get_verbs():
    with open("static/sentences.json", encoding='UTF8') as config_file:         # 인코딩 에러 -   encoding='UTF8' 필요
        data = json.load(config_file)
        verbs = [key for key in data["Sentences"]]                              # json 읽고, 그 안에 "Sentences" 안에 키값만 가져옴 즉, 동사 리스트 가져오기 Key = verbs, value = sentences of the verb
        return verbs

def get_sentence(verb):
    with open("static/sentences.json", encoding='UTF8') as config_file:
        data = json.load(config_file)
        return data["Sentences"][verb], data["Explanation"][verb]                # input = verb, output = the sentence, explanation of the verb

def disorder_sentence(sen1):
    sentence = sen1
    sentence_words = sentence.split(' ')
    n = len(sentence_words)
    new_sentence = []
    while n > 0:
        number = random.randint(0, n - 1)
        new_sentence.append(sentence_words[number])
        sentence_words.pop(number)
        n = len(sentence_words)
    return new_sentence

def get_data(verb):
    sen1, exp1 = get_sentence(verb)
    rd_sen = disorder_sentence(sen1)
    r_n = len(rd_sen)
    return sen1, exp1, rd_sen, r_n           # input = verb, output = the sentence, explanation of the verb, disorder_sentence of the sentence, the length of disorder_sentence

def get_random_verb():
    verbs = get_verbs()
    n = len(verbs)
    r_n = random.randint(0,n-1)
    verb = verbs[r_n]
    return verb

@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route("/verb")
def verb_random():
    verb = get_random_verb()
    form = input_sentent_Form(request.form)
    sen1, exp1, rd_sen, r_n = get_data(verb)
    return render_template('verb.html', form=form, rd_sen=rd_sen, r_n=r_n, exp1=exp1, verb=verb, sen=sen1)

@app.route("/verb/<string:verb>", methods=["GET", "POST"])
def verb(verb):
    form = input_sentent_Form(request.form)
    sen1, exp1, rd_sen, r_n = get_data(verb)
    if request.method == "POST" and form.validate():
        sentence_in = form.sentence_input.data
        if sen1 == sentence_in:
            flash('Correct')
            return redirect(url_for('verb_random'))
        else:
            flash('Wrong')
            return render_template('verb.html', form=form, rd_sen=rd_sen, r_n=r_n, exp1=exp1, verb=verb, sen=sen1)
    elif request.method == "POST":
        flash('Try again. (Nothing is submitted.)')
        return render_template('verb.html', form=form, rd_sen=rd_sen, r_n=r_n, exp1=exp1, verb=verb, sen=sen1)

    else:
        return render_template('verb.html', form=form, rd_sen=rd_sen, r_n=r_n, exp1=exp1, verb=verb, sen=sen1)

@app.context_processor                # verbs, n = global var
def context_processor():
    verbs = get_verbs()
    shuffle(verbs)
    n = len(verbs)
    return dict(verbs=verbs, n=n)

if __name__ == '__main__':
    app.run(debug=True) # , host='0.0.0.0', port=5001

