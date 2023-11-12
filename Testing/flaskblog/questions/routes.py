from flask import render_template, request, redirect, url_for
from models import db, User, UserAnswer, Question
from forms import UserAnswerForm

questions = Blueprint('questions', __name__)

@questions.route("/test/<int:audio_file_id>", methods=['GET', 'POST'])
@login_required
def test_questions(audio_file_id):
    user = User.query.filter_by(username=username).first()
    audio_file = AudioFile.query.get_or_404(audio_file_id)

    if user:
        form = UserAnswerForm()

        if form.validate_on_submit():
            user_answer = UserAnswer(
                user_id=user.id,
                question_id=audio_file.questions[0].id,  # Assuming all questions share the same ID
                enjoyment_rating=form.enjoyment_rating.data,
                genre_rating=form.genre_rating.data if form.genre_rating.data != 'not_sure' else None,
                mood_rating=form.mood_rating.data if form.mood_rating.data != 'not_sure' else None,
                vocal_timbre_rating=form.vocal_timbre_rating.data if form.vocal_timbre_rating.data != 'not_sure' else None
            )

            db.session.add(user_answer)
            db.session.commit()

            return redirect(url_for('questions.test_questions', audio_file_id=audio_file_id))

        return render_template('user_info.html', username=username, form=form, audio_file=audio_file)

    return "User not found"
