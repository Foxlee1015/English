from wtforms import Form, SubmitField, TextAreaField, validators


class input_sentence_Form(Form):
    sentence_input = TextAreaField('input', [validators.Length(min=1, max=100)])
    submit = SubmitField('문장 제출')

class search_word_Form(Form):
    word = TextAreaField('words', [validators.Length(min=1, max=10)])
    submit = SubmitField('단어 검색')
