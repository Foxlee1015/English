from flask import Flask
from english.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SESSION_TYPE'] = 'filesystem'
    UPLOAD_FOLDER = 'static/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from english.main.routes import main
    from english.verb.routes import verb_b
    from english.audio.routes import audio_b
    from english.models import models

    app.register_blueprint(main)
    app.register_blueprint(verb_b)
    app.register_blueprint(audio_b)
    app.register_blueprint(models)

    return app