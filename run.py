import os
from flask import Flask, render_template, request, flash, url_for, redirect
from wtforms import Form, SubmitField, TextAreaField, validators, FileField
import random, json
from random import shuffle
from bs4 import BeautifulSoup
import urllib.request
from flask_restful import Resource, Api, reqparse
from flask_wtf.file import FileAllowed  # FileRequired
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
api = Api(app)


UPLOAD_FOLDER = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class AudioForm(Form):
    audio1 = TextAreaField('What audio', [validators.data_required(), validators.Length(min=1, max=20)])
    audio2 = FileField('Audio file', validators=[FileAllowed(['mp3', 'mp4', 'wma'])])
    submit = SubmitField('okay')

class Verb_list(Resource):
    def get(self):
        with open("static/sentences.json", encoding='UTF8') as f1:
            data1 = json.load(f1)
        with open('static/meaning.json', encoding='utf-8') as f2:
            data2 = json.load(f2)
        data1.update(data2)
        return data1

class Verb_search(Resource):
    def get(self,verb):
        try:
            sentence, explanation = get_sentence(verb)
            meaning = Get_meaning(verb)
            return {'verb': verb, "meaning": meaning, "quiz": sentence, "explanation": explanation } #, 'email': email}
        except: # 단어가 저장되어 있지 않은 경우
            meaning = Get_meaning(verb)
            return {'verb': verb, "meaning": meaning}
    #POST 방식 - 클라이언트가 단어 전송
    def post(self, verb):
        parser = reqparse.RequestParser()
        parser.add_argument('verb', type=str)
        args = parser.parse_args('verb')
        verb = args['verb']
        try:
            sentence, explanation = get_sentence(verb)
            meaning = Get_meaning(verb)
            return {'verb': verb, "meaning": meaning, "quiz": sentence, "explanation": explanation } #, 'email': email}
        except: # 단어가 저장되어 있지 않은 경우
            meaning = Get_meaning(verb)
            return {'verb': verb, "meaning": meaning}

api.add_resource(Verb_list, '/verb_list')
api.add_resource(Verb_search, '/verb_search/<string:verb>')

class input_sentence_Form(Form):
    sentence_input = TextAreaField('input', [validators.Length(min=1, max=100)])
    submit = SubmitField('문장 제출')

class search_word_Form(Form):
    word = TextAreaField('words', [validators.Length(min=1, max=10)])
    submit = SubmitField('단어 검색')

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
    audio_form = AudioForm(request.form)
    search_form = search_word_Form(request.form)
    if request.method == "POST" and search_form.validate():
        word = search_form.word.data
        word_meaning = Get_meaning(word)
        return render_template('home.html', word_meaning=word_meaning, search_form=search_form, audio_form=audio_form)
    else:
        return render_template('home.html', search_form=search_form, audio_form=audio_form)

@app.route("/audio/register", methods=["GET", "POST"])
def audio():
    audio_form = AudioForm(request.form)
    if request.method == "POST" and audio_form.validate():
        print('성공')
        file = request.files['file']  # post 된 파일 정보 가져옴
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('audio.html', audio_form=audio_form)
    else:
        return render_template('audio.html', audio_form=audio_form)

@app.route("/audio/list", methods=["GET", "POST"])
def audio_list():
    return render_template('audio_list.html')



@app.route("/verb")
def verb_random():
    verb = get_random_verb()
    input_form = input_sentence_Form(request.form)
    search_form = search_word_Form(request.form)
    sen1, exp1, rd_sen, r_n = get_data(verb)
    meaning = Get_meaning(verb)
    return render_template('verb.html', input_form=input_form, search_form=search_form, rd_sen=rd_sen, r_n=r_n, exp1=exp1, verb=verb, sen=sen1, meaning=meaning)

@app.route("/verb/<string:verb>", methods=["GET", "POST"])
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

@app.context_processor                # verbs, n = global var
def context_processor():
    verbs = get_verbs()
    shuffle(verbs)
    n = len(verbs)
    return dict(verbs=verbs, n=n)

def Get_dicionary_meaing(verb):
    try:
        with urllib.request.urlopen("https://dictionary.cambridge.org/dictionary/english/"+verb) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            meaning = soup.find('b', {'class':'def'})
            if meaning == None:
                return None
            else:
                meaning = meaning.get_text()
                print(meaning)
                return meaning
    except:
        return None

def Get_meaning(verb):
    with open('static/meaning.json', 'r', encoding='utf-8') as f1:
        m_data = json.load(f1)  # 기존 데이터
        try:
            meaning = m_data[verb]
            return meaning
        except: # 크롤링 업데이트
            meaning = Get_dicionary_meaing(verb)
            data = {verb: meaning}
            m_data.update(data)    # 데이터 추가
            with open('static/meaning.json', 'w', encoding='utf-8') as f1:
                json.dump(m_data, f1) # 저장
                return meaning

if __name__ == '__main__':
    app.run(debug=True) # , host='0.0.0.0', port=5001

