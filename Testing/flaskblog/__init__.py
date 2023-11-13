from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bycrpt
from flask_login import LoginManager
#from flask_mail import Mail
from flaskblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
#mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    #mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    #from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(questions)
    app.register_blueprint(main)
    #app.register_blueprint(errors)

    with app.app_context():
        # Create instances of AudioFile and add them to the database
        from flaskblog.models import AudioFile

        audio_files_directory = 'static/audio/'

        for order, file_name in enumerate(os.listdir(audio_files_directory), start=1):
            file_path = os.path.join(audio_files_directory, file_name)
            audio_file = AudioFile(file_path=file_path, order=order)
            db.session.add(audio_file)
        
        db.session.commit()

    return app
