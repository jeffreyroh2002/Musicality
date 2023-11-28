from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.fields import IntegerRangeField

class UserAnswerForm(FlaskForm):
    overall_rating = SelectField('How much did you enjoy this song? (Scale of 1 to 5)', choices=[(1, '-2'), (2, '-1'), (3, '0'), (4, '1'), (5, '2')])
    genre_rating = SelectField('How much did Genre play a role in your rating above? (Scale of 1 to 5)', choices=[(1, '-2'), (2, '-1'), (3, '0'), (4, '1'), (5, '2'), ('not_sure', 'Not sure')])
    mood_rating = SelectField('How much did the Mood of the song play a role in your rating above? (Scale of 1 to 5)', choices=[(1, '-2'), (2, '-1'), (3, '0'), (4, '1'), (5, '2'), ('not_sure', 'Not sure')])
    vocal_timbre_rating = SelectField('How much did the Vocal Timbre of the song play a role in your rating above? (Scale of 1 to 5)', choices=[(1, '-2'), (2, '-1'), (3, '0'), (4, '1'), (5, '2'), ('not_sure', 'Not sure')])
    submit = SubmitField('Submit')