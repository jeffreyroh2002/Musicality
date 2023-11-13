from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from models import db, UserAnswer, AudioFile
from forms import UserAnswerForm

def get_next_audio_file_id(current_audio_file_id):
    current_audio_file = AudioFile.query.get_or_404(current_audio_file_id)
    next_audio_file = AudioFile.query.filter(AudioFile.order > current_audio_file.order).order_by(AudioFile.order.asc()).first()

    if next_audio_file:
        return next_audio_file.id
    else:
        return None

questions = Blueprint('questions', __name__)

@questions.route("/test/<int:audio_file_id>", methods=['GET', 'POST'])
@login_required
def test_questions(audio_file_id):
    user = current_user
    audio_file = AudioFile.query.get_or_404(audio_file_id)
    form = UserAnswerForm()

    if form.validate_on_submit():
        user_answer = UserAnswer(
            user_id=user.id,
            question_id=audio_file.questions[0].id,
            enjoyment_rating=form.enjoyment_rating.data,
            genre_rating=form.genre_rating.data if form.genre_rating.data != 'not_sure' else None,
            mood_rating=form.mood_rating.data if form.mood_rating.data != 'not_sure' else None,
            vocal_timbre_rating=form.vocal_timbre_rating.data if form.vocal_timbre_rating.data != 'not_sure' else None
        )

        db.session.add(user_answer)
        db.session.commit()

        next_audio_file_id = get_next_audio_file_id(audio_file_id)
        if next_audio_file_id is not None:
            return redirect(url_for('questions.test_questions', audio_file_id=next_audio_file_id))

    return render_template('questionnaire.html', form=form, audio_file=audio_file)

@questions.route("/survey-completed", methods=['GET'])
def survey_completed():
    return render_template('survey_completed.html')