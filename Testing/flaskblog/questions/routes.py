from flask import render_template, request, redirect, url_for
from models import db, User, UserAnswer, Question
from forms import UserAnswerForm

questions = Blueprint('questions', __name__)

@questions.route("/test", methods=['GET', 'POST'])
@login_required
def test_questions():
    user = User.query.filter_by(username=username).first()

    if user:
        # Get all questions for the user -> change to one each in future
        questions = Question.query.all()

        form = UserAnswerForm()

        if form.validate_on_submit():
            for question in questions:
                user_answer = UserAnswer(
                    user_id=user.id,
                    question_id=question.id,
                    enjoyment_rating=getattr(form, f'question_{question.id}').data,
                    genre_rating=getattr(form, f'question_{question.id}').data if getattr(form, f'question_{question.id}').data != 'not_sure' else None,
                    mood_rating=getattr(form, f'question_{question.id}').data if getattr(form, f'question_{question.id}').data != 'not_sure' else None,
                    vocal_timbre_rating=getattr(form, f'question_{question.id}').data if getattr(form, f'question_{question.id}').data != 'not_sure' else None
                )
                
                db.session.add(user_answer)
                db.session.commit()

            return redirect(url_for(questions.test_questions))

        return render_template('user_info.html', username=username, questions=questions, form=form)

    return "User not found"