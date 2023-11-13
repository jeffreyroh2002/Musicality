from flask import Flask
#from flaskblog.extensions import db, bcrypt, login_manager, mail
from flaskblog.extensions import db, bcrypt, login_manager
from flaskblog.config import Config
from flaskblog.questions.routes import questions
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    # Uncomment the following line when you want to use Flask-Mail
    # mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(questions)
    app.register_blueprint(main)

    with app.app_context():
        from flaskblog.models import AudioFile
        audio_files_directory = os.path.join(os.getcwd(), 'flaskblog', 'static', 'audio')
        for order, file_name in enumerate(os.listdir(audio_files_directory), start=1):
            file_path = os.path.join(audio_files_directory, file_name)
            audio_file = AudioFile(file_path=file_path, order=order)
            db.session.add(audio_file)
        db.session.commit()

    return app