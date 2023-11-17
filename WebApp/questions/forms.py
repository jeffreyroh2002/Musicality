from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField

class UserAnswerForm(FlaskForm):
    overall_rating = IntegerField('How much did you enjoy this song? (Scale of 1 to 5)')
    genre_rating = IntegerField('How much did Genre play a role in your rating above? (Scale of 1 to 5)', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), ('not_sure', 'Not sure')])
    mood_rating = IntegerField('How much did the Mood of the song play a role in your rating above? (Scale of 1 to 5)', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), ('not_sure', 'Not sure')])
    vocal_timbre_rating = IntegerField('How much did the Vocal Timbre of the song play a role in your rating above? (Scale of 1 to 5)', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), ('not_sure', 'Not sure')])
    submit = SubmitField('Submit')