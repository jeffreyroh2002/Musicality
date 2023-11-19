from flask import render_template, redirect, url_for, Blueprint, flash
from flask_login import current_user, login_required
from WebApp.models import db, UserAnswer, AudioFile, Test
from .forms import UserAnswerForm  #.forms imports from same package dir
from datetime import datetime

def get_next_audio_file_id(current_audio_file_id):
    current_audio_file = AudioFile.query.get_or_404(current_audio_file_id)
    next_audio_file = AudioFile.query.filter(AudioFile.id > current_audio_file.id).order_by(AudioFile.id.asc()).first()

    if next_audio_file:
        return next_audio_file.id
    else:
        return None

questions = Blueprint('questions', __name__)

@questions.route("/test/<int:test_type>/<int:audio_file_id>", methods=['GET', 'POST'])
@login_required
def test_questions(test_type, audio_file_id):

    user = current_user
    test = Test.query.filter((Test.user_id==user.id) & (Test.test_type==test_type)).first()

    if audio_file_id == 0:
        # haven't taken this test before (new user)
        if not test:
            # add new test data to Test model
            test_val = Test(
                test_type = test_type,
                test_start_time = datetime.now(),
                subject = user
            )
            db.session.add(test_val)
            db.session.commit()

            return redirect(url_for('questions.test_questions', test_type=test_type, audio_file_id=1))

        
        latest_answer = UserAnswer.query.filter_by(user=current_user).order_by(UserAnswer.audio_id.desc()).first()
        latest_audio_num = latest_answer.audio_id
        
        # when you have already finished this type of test
        if len(AudioFile.query.all()) == latest_audio_num:
            flash('You have already taken this test!', 'info')
            return redirect(url_for('questions.survey_completed'))
        else:
            flash('It seems you have already answers some questions in the past. Starting where you left off.', 'info')
            return redirect(url_for('questions.test_questions', test_type=test_type, audio_file_id=latest_audio_num+1))
    
    audio_file = AudioFile.query.get_or_404(audio_file_id)
    form = UserAnswerForm()

    if form.validate_on_submit():
        user_answer = UserAnswer(
            overall_rating=form.overall_rating.data,
            genre_rating=form.genre_rating.data if form.genre_rating.data != 'not_sure' else -1,
            mood_rating=form.mood_rating.data if form.mood_rating.data != 'not_sure' else -1,
            vocal_timbre_rating=form.vocal_timbre_rating.data if form.vocal_timbre_rating.data != 'not_sure' else -1,
            user = current_user,
            audio = audio_file,
            test = test
        )

        db.session.add(user_answer)
        db.session.commit()

        next_audio_file_id = get_next_audio_file_id(audio_file_id)

        if next_audio_file_id is not None:
            return redirect(url_for('questions.test_questions', test_type=test_type, audio_file_id=next_audio_file_id))
        else:
            # save the end time, when finishing the test
            test.test_end_time = datetime.now()
            db.session.commit()

            return redirect(url_for('questions.survey_completed'))

    return render_template('questionnaire.html', form=form, audio_file=audio_file)

@questions.route("/survey-completed", methods=['GET'])
def survey_completed():

    return render_template('survey_completed.html')