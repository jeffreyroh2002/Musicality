from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.fields import IntegerRangeField

class UserAnswerForm(FlaskForm):
    overall_rating = SelectField('How much did you enjoy this song? (Scale of 1 to 7)', choices=[(-3, 'Strongly Negative'), (-2, 'Negative'), (-1, 'Slightly Negative'), (0, 'Average'), (1, 'Slightly Positive'), (2, 'Positive'), (-3, 'Strongly Positive')])
    genre_rating = SelectField('How would you rate the Genre? (Scale of 1 to 7)', choices=[(-3, 'Strongly Negative'), (-2, 'Negative'), (-1, 'Slightly Negative'), (0, 'Average'), (1, 'Slightly Positive'), (2, 'Positive'), (-3, 'Strongly Positive')])
    mood_rating = SelectField('How would you rate the Mood?(Scale of 1 to 7)', choices=[(-3, 'Strongly Negative'), (-2, 'Negative'), (-1, 'Slightly Negative'), (0, 'Average'), (1, 'Slightly Positive'), (2, 'Positive'), (-3, 'Strongly Positive')])
    vocal_timbre_rating = SelectField('How would you rate the Vocals if present? (Scale of 1 to 7)', choices=[(-3, 'Strongly Negative'), (-2, 'Negative'), (-1, 'Slightly Negative'), (0, 'Average'), (1, 'Slightly Positive'), (2, 'Positive'), (-3, 'Strongly Positive')])
    submit = SubmitField('Submit')