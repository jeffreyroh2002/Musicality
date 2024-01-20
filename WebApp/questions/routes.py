from flask import render_template, redirect, url_for, Blueprint, flash, request
from flask_login import current_user, login_required
from WebApp.models import db, UserAnswer, AudioFile, Test
from .forms import UserAnswerForm  #.forms imports from same package dir
from datetime import datetime

questions = Blueprint('questions', __name__)

@questions.route("/before-test/<int:test_type>")
@login_required
def before_test(test_type):
    return render_template("before_test.html", test_type=test_type)

def get_next_audio_file_id(current_audio_file_id):
    current_audio_file = AudioFile.query.get_or_404(current_audio_file_id)
    next_audio_file = AudioFile.query.filter(AudioFile.id > current_audio_file.id).order_by(AudioFile.id.asc()).first()

    if next_audio_file:
        return next_audio_file.id
    else:
        return None


@questions.route("/test/<int:test_type>/<int:audio_file_id>", methods=['GET', 'POST'])
@login_required
def test_questions(test_type, audio_file_id):

    user = current_user
    # we also have to consider the case that a user already have taken a specific type of test, and need additional test.
    test = Test.query.filter((Test.user_id==user.id) & (Test.test_type==test_type)).order_by(Test.test_start_time.desc()).first()

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
    
        # already have taken this test before (start new test)
        if test.test_end_time:
            # add new test data to Test model
            test_val = Test(
                test_type = test_type,
                test_start_time = datetime.now(),
                subject = user
            )
            db.session.add(test_val)
            db.session.commit()

            flash('You have already taken this type of test before. Start test again.', 'info')
            return redirect(url_for('questions.test_questions', test_type=test_type, audio_file_id=1))

        
        latest_answer = UserAnswer.query.filter((UserAnswer.user==current_user) & (UserAnswer.test==test)).order_by(UserAnswer.audio_id.desc()).first()
        if not latest_answer :
            return redirect(url_for('questions.test_questions', test_type=test_type, audio_file_id=1))
        latest_audio_num = latest_answer.audio_id
        
        # when you have already finished this type of test
        if len(AudioFile.query.all()) == latest_audio_num:
            flash('You have already taken this test!', 'info')
            return redirect(url_for('results.single_test_result', test_id=test.id))
        else:
            flash('It seems you have already answers some questions in the past. Starting where you left off.', 'info')
            return redirect(url_for('questions.test_questions', test_type=test_type, audio_file_id=latest_audio_num+1))
    
    audio_file = AudioFile.query.get_or_404(audio_file_id)
    form = UserAnswerForm()
    db_answer = UserAnswer.query.filter((UserAnswer.test == test) & (UserAnswer.audio == audio_file) & (UserAnswer.user == current_user)).first()

    if form.validate_on_submit():
        # when answer fields exists after next button
        if db_answer:
            db_answer.overall_rating=form.overall_rating.data
            db_answer.genre_rating=form.genre_rating.data
            db_answer.genre_not_sure=form.genre_not_sure.data 
            db_answer.mood_rating=form.mood_rating.data
            db_answer.mood_not_sure=form.mood_not_sure.data 
            db_answer.vocal_timbre_rating=form.vocal_timbre_rating.data
            db_answer.vocal_not_sure=form.vocal_not_sure.data 

        # when answer fields do not exists after next button
        else:
            user_answer = UserAnswer(
                overall_rating=form.overall_rating.data,
                genre_rating=form.genre_rating.data,
                genre_not_sure=form.genre_not_sure.data, 
                mood_rating=form.mood_rating.data,
                mood_not_sure=form.mood_not_sure.data, 
                vocal_timbre_rating=form.vocal_timbre_rating.data,
                vocal_not_sure=form.vocal_not_sure.data,

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

            return redirect(url_for('results.single_test_result', test_id=test.id))
    
    # when press prev button
    elif request.method == 'GET' and db_answer:
        form.overall_rating.default = db_answer.overall_rating
        form.genre_rating.default = db_answer.genre_rating
        form.mood_rating.default = db_answer.mood_rating
        form.vocal_timbre_rating.default = db_answer.vocal_timbre_rating
        if db_answer.genre_not_sure:
            form.genre_not_sure.default = True
        if db_answer.mood_not_sure:
            form.mood_not_sure.default = True
        if db_answer.vocal_not_sure:
            form.vocal_not_sure.default = True
        form.process()


    

    return render_template('questionnaire.html', form=form, test_type=test_type, audio_file=audio_file, test=test)

@questions.route("/survey-completed/<int:test_id>", methods=['GET'])
def survey_completed(test_id):
    ### Instead Render new template that is a loading screen. "Hang in there..."
    #return render_template('survey_completed.html')

    #for now, instantly direct to test_results route

    # in this URL, we should show thankful comments & loading screens with a new HTML page
    return redirect(url_for('results.single_test_result', test_id=test_id))