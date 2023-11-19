from flask import render_template, redirect, url_for, Blueprint, flash
from flask_login import current_user, login_required
from WebApp.models import db, Test, UserAnswer, AudioFile
from .forms import UserAnswerForm  #.forms imports from same package dir

results = Blueprint('results', __name__)

@results.route("/test-results/<test_id>", methods=['GET', 'POST'])
@login_required
def show_results(test_id): 

