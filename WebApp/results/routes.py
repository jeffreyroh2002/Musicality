from flask import render_template, redirect, url_for, Blueprint, flash, abort
from flask_login import current_user, login_required
from WebApp.models import db, Test, UserAnswer, AudioFile
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
    if test.subject != current_user: 
        abort(403)

    
    #Update Preference each Song
    genre_score = {'Blues': 0, 'Ballad': 0, 'Orchestral': 0, 'Country': 0,
                    'Electronic': 0, 'HipHop': 0, 'Jazz': 0, 'Metal': 0, 
                    'Pop': 0, 'Reggae': 0, 'Rock': 0, 'RB_Soul': 0}
    mood_score = {'Angry': 0, 'Bright': 0, 'Melancholic': 0, 'Relaxed': 0}
    vocal_score = {'Smooth': 0,'Dreamy': 0,'Raspy': 0,'Voiceless': 0}

    answers = UserAnswer.query.filter_by(test_id=test_id).all()
    for answer in answers:
        audio = AudioFile.query.get(answer.audio_id)

        #from audioFile model
        genre_pred = audio.genre   #assuming audioFile is populated with scores using dictionaries with same keys
        mood_pred = audio.mood
        vocal_pred = audio.vocal

        #from Questions Form
        overall_rating = answer.overall_rating   # need to use this
        genre_rating = answer.genre_rating
        mood_rating = answer.mood_rating
        vocal_rating = answer.vocal_rating

        #Calculate each genre score
        genre_weighted = {}
        if genre_pred and not isinstance(audio.genre, float):
            genre_scores = audio.genre
            try:
                genre_data = json.loads(genre_scores)
            except json.JSONDecodeError:
                print("Error decoding genre_data JSON.")

            for genre_name, proportion in genre_data.items():
                genre_weighted[genre_name] = proportion * genre_rating
            
            for genre in genre_weighted:
                genre_score[genre] += genre_weighted[genre]

        else:
            print("Genre data is not available or is in an unexpected format.")

        #Calculate each mood score
        mood_weighted = {}
        if mood_pred and not isinstance(audio.mood, float):
            mood_scores = audio.mood
            try:
                mood_data = json.loads(mood_scores)
            except json.JSONDecodeError:
                print("Error decoding mood_data JSON.")

            for mood_name, proportion in mood_data.items():
                mood_weighted[mood_name] = proportion * mood_rating
            
            for mood in mood_weighted:
                mood_score[mood] += mood_weighted[mood]

        else:
            print("Mood data is not available or is in an unexpected format.")

        #Calculate each vocal timbre score
        vocal_weighted = {}
        if vocal_pred and not isinstance(audio.vocal, float):
            vocal_scores = audio.vocal
            try:
                vocal_data = json.loads(vocal_scores)
            except json.JSONDecodeError:
                print("Error decoding vocal_data JSON.")

            for vocal_name, proportion in vocal_data.items():
                vocal_weighted[vocal_name] = proportion * vocal_rating
            
            for vocal in vocal_weighted:
                vocal_score[vocal] += vocal_weighted[vocal]
        else:
            print("Vocal data is not available or is in an unexpected format.")
        
    return render_template('single_test_result.html', user=user, test=test, genre_score=genre_score, mood_score=mood_score, vocal_score=vocal_score)
    


@results.route("/test-results/<int:user_id>", methods=['GET', 'POST'])
@login_required
def show_user_results():
    # load all of users previous tests -> might want to add this to user instead



