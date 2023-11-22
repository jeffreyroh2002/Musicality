from flask import render_template, redirect, url_for, Blueprint, flash
from flask_login import current_user, login_required
from WebApp.models import db, Test, UserAnswer, AudioFile, Test
from .forms import UserAnswerForm  #.forms imports from same package dir

"""
results = Blueprint('results', __name__)
@results.route("/test-results/<int:user_id>/<int:test_id>", methods=['GET', 'POST'])
@login_required
def show_single_result(test_id):
    #calculate all all characteristics
    
    user = current_user
    test = Test.query.filter((Test.user_id==current_user.id) & Test_test_type==1)
"""

results = Blueprint('results', __name__)
@results.route("/test-results/<int:test_id>", methods=['GET', 'POST'])
@login_required
def single_test_result(test_id):
    #calculate all characteristics
    user = current_user
    test = Test.query.filter_by(id=test_id).first()
    if test.subject != current_user: abort(403)

    """
    answers = test.answers
    test_type = test.test_type
    """

    #Update Preference each Song
    genre_score = {'Blues': 0, 'Ballad': 0, 'Classical': 0, 'Country': 0,
                    'Electronic': 0, 'HipHop': 0, 'Jazz': 0, 'Metal': 0, 
                    'Pop': 0, 'Reggae': 0, 'Rock': 0, 'Soul/R&B': 0}
    mood_score = {'Angry': 0, 'Bright': 0, 'Melancholy': 0, 'Relaxed': 0}
    vocal_score = {'Clear': 0,'Ethereal': 0,'Raspy': 0}

    for answer in UserAnswers:
        audio = answer.audio_id

        genre_pred = audio.genre   #assuming audioFile is populated with scores using dictionaries with same keys
        mood_pred = audio.mood
        vocal_pred = audio.vocal

        overall_rating = answer.overall_rating
        genre_rating = answer.genre_rating
        mood_rating = answer.mood_rating
        vocal_rating = answer.vocal_rating

        genre_weighted = {key: value * genre_rating for key, value in genre_pred.items()}
        mood_weighted = {key: value * mood_rating for key, value in mood_pred.items()}
        vocal_weighted = {key: value * vocal_rating for key, value in vocal_pred.items()}

        for genre in genre_weighted:
            genre_score[genre] += genre_weighted[genre]

        for mood in mood_weighted:
            mood_score[mood] += mood_weighted[mood]

        for vocal in vocal_weighted:
            vocal_score[vocal] += vocal_weighted[vocal]
        
    return render_template('single_test_result.html', user=user, test=test, genre_score=genre_score, mood_score=mood_score, vocal_score=vocal_score)
    


@results.route("/test-results/<int:user_id>", methods=['GET', 'POST'])
@login_required
def show_user_results():
    # load all of users previous tests -> might want to add this to user instead



