from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable=False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable= False)
    answers = db.relationship('UserAnswer', backref = 'user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class AudioFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    questions = db.relationship('Question', backref='audio_file', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    audio_file_id = db.Column(db.Integer, db.ForeignKey('audio_file.id'), nullable=False)
    user_answers = db.relationship('UserAnswer', backref='question', lazy=True)

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    overall_rating = db.Column(db.Integer, nullable=False)
    genre_rating = db.Column(db.Integer, nullable=True)
    mood_rating = db.Column(db.Integer, nullable=True)
    vocal_rating = db.Column(db.Integer, nullable=True)


    def __repr__(self):
        return f"<UserAnswer {self.id} - User: {self.user.username}, Question ID: {self.question_id}>"
