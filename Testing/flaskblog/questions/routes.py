from flask import render_template, request, redirect, url_for
from models import db, User, UserAnswer, Question
from forms import UserAnswerForm

questions = Blueprint('questions', __name__)

@questions.route("/test", methods=['GET', 'POST'])
def test_questions():
    user = User.query.filter_by(username=username).first()

    if user:
        # Get all questions for the user
        questions = Question.query.all()

        if request.method == 'POST':
            form = UserAnswerForm(request.form)

            if form.validate():
                for question in questions:
                    user_answer = UserAnswer(
                        user_id=user.id,
                        question_id=question.id,
                        enjoyment_rating=form.enjoyment_rating.data,
                        genre_rating=form.genre_rating.data if form.genre_rating.data != 'not_sure' else None,
                        mood_rating=form.mood_rating.data if form.mood_rating.data != 'not_sure' else None,
                        vocal_timbre_rating=form.vocal_timbre_rating.data if form.vocal_timbre_rating.data != 'not_sure' else None
                    )

                    db.session.add(user_answer)
                    db.session.commit()

                return redirect(url_for('users.user_info', username=username))

        else:
            # Dynamically generate form fields based on questions
            form = UserAnswerForm()
            for question in questions:
                setattr(form, f'question_{question.id}', IntegerField(question.text, choices=[(i, str(i)) for i in range(1, 6)] + [('not_sure', 'Not sure')]))

        return render_template('user_info.html', username=username, questions=questions, form=form)

    return "User not found"
