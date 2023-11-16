from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from WebApp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=True)
    tests = db.relationship("Test", backref="subject", lazy=True)
    answers = db.relationship("UserAnswer", backref="user", lazy=True)

    def get_reset_token(self, expires_sec=600):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(30), nullable=False)
    test_date = db.Column(db.Datetime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Test('{self.user_id}', '{self.test_name}', '{self.test_date}')"


class AudioFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    audio_name = db.Column(db.String(20), nullable=False)
    audio_path = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.Text, nullable=False)  # json.dump로 dict type 처리 후 save
    mood = db.Column(db.Text, nullable=False)
    vocal = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"AudioFile('{self.audio_name}', '{self.audio_path}', '{self.genre}', '{self.mood}', '{self.vocal}')"


class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    overall_rating = db.Column(db.Integer, nullable=False)
    genre_rating = db.Column(
        db.Integer, nullable=False
    )  # if user check "I don't know" == -1
    mood_rating = db.Column(db.Integer, nullable=False)
    vocal_rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    audio_id = db.Column(db.Integer, db.ForeignKey("audiofile.id"), nullable=False)

    def __repr__(self):
        return (
            f"UserAnswer('{self.user_id}', '{self.audio_id}', '{self.overall_rating}')"
        )
