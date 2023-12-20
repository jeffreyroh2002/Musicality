import json
from flask import render_template, redirect, url_for, Blueprint, flash, abort
from flask_login import current_user, login_required
from WebApp.models import db, Test, UserAnswer, AudioFile
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict
import statistics
import matplotlib.pyplot as plt

#imports for saving png files
import io
import base64
import matplotlib.pyplot as plt
from flask import render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator
from collections import defaultdict
import seaborn as sns


# Set matplotlib style
plt.style.use('ggplot')

"""
results = Blueprint('results', __name__)
@results.route("/test-results/<int:user_id>/<int:test_id>", methods=['GET', 'POST'])
@login_required
def show_single_result(test_id):
    #calculate all all characteristics
    
    user = current_user
    test = Test.query.filter((Test.user_id==current_user.id) & Test_test_type==1)
"""

def get_attribute_name(index):
    # Define the order of attributes in your feature vectors
    attributes = ['Rock','Hip Hop','Pop Ballad','Electronic','Korean Ballad','Jazz','R&B/Soul', 
                  'Tense', 'Bright', 'Emotional', 'Relaxed', 
                  'Smooth', 'Dreamy', 'Raspy', 'Voiceless']
    
    # Return the attribute name corresponding to the given index
    return attributes[index]

results = Blueprint('results', __name__)
@results.route("/test-results/<int:test_id>", methods=['GET', 'POST'])
@login_required
def single_test_result(test_id):
    
    display_messages = []

    #calculate all characteristics
    user = current_user
    test = Test.query.filter_by(id=test_id).first()
    if test.subject != current_user: 
        abort(403)

    
    #Update Preference each Song
    genre_score = {'Rock': 0,'Hip Hop': 0,'Pop Ballad': 0,'Electronic': 0,'Korean Ballad': 0,'Jazz': 0,'R&B/Soul': 0}
    mood_score = {'Angry': 0, 'Bright': 0, 'Melancholic': 0, 'Relaxed': 0}
    vocal_score = {'Smooth': 0,'Dreamy': 0,'Raspy': 0,'Voiceless': 0}

    # High Rating song tracker
    high_rated_songs = []

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
        genre_not_sure = answer.genre_not_sure
        mood_rating = answer.mood_rating
        mood_not_sure = answer.mood_not_sure
        vocal_rating = answer.vocal_timbre_rating
        vocal_not_sure = answer.vocal_not_sure

        #Calculate overall score
        #Calculate each genre score
        genre_weighted = {}
        if genre_pred and not isinstance(audio.genre, float):
            genre_scores = audio.genre
            try:
                genre_data = json.loads(genre_scores)
            except json.JSONDecodeError:
                print("Error decoding genre_data JSON.")

            #if user is not sure about the genre, calculate the genre_score based on overall rating
            if genre_not_sure:
                for genre_name, proportion in genre_data.items():
                    genre_weighted[genre_name] = proportion * overall_rating
            
            #in other case, calculate the genre_score based on (0.3 portion of overall_rating) and (0.7 portion of genre_rating)
            else:
                for genre_name, proportion in genre_data.items():
                    genre_weighted[genre_name] = (proportion * overall_rating * 0.3) + (proportion * genre_rating * 0.7)

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

            #if user is not sure about the mood, calculate the mood_score based on overall rating
            if mood_not_sure:
                for mood_name, proportion in mood_data.items():
                    mood_weighted[mood_name] = proportion * overall_rating
            
            #in other case, calculate the mood_score based on (0.3 portion of overall_rating) and (0.7 portion of mood_rating)
            else:
                for mood_name, proportion in mood_data.items():
                    mood_weighted[mood_name] = (proportion * overall_rating * 0.3) + (proportion * mood_rating * 0.7)
            
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

            #if user is not sure about the vocal, calculate the vocal_score based on overall rating
            if vocal_not_sure:
                for vocal_name, proportion in vocal_data.items():
                    vocal_weighted[vocal_name] = proportion * overall_rating
            
            #in other case, calculate the vocal_score based on (0.3 portion of overall_rating) and (0.7 portion of vocal_rating)
            else:
                for vocal_name, proportion in vocal_data.items():
                    vocal_weighted[vocal_name] = (proportion * overall_rating * 0.3) + (proportion * vocal_rating * 0.7)
                    
            for vocal in vocal_weighted:
                vocal_score[vocal] += vocal_weighted[vocal]
        else:
            print("Vocal data is not available or is in an unexpected format.")
        
    # store highly rated songs into high_rated songs list
        if (overall_rating >= 2):
            high_rated_songs.append(answer.audio_id)

    # array of arrays to store each feature vector of highly rated songs
    high_rated_feature_vectors = []
    for high_rated_song in high_rated_songs:
        audio = AudioFile.query.get(high_rated_song)
        genre_data = json.loads(audio.genre)
        mood_data = json.loads(audio.mood)
        vocal_data = json.loads(audio.vocal)

        # print("genre data", genre_data)
        # print("mood data", mood_data)
        # print("vocal data", vocal_data)

        # Flatten the dictionaries into a single array
        feature_vector = list(genre_data.values()) + list(mood_data.values()) + list(vocal_data.values())

        # Normalize the feature vector
        normalized_vector = normalize([feature_vector])[0]
        high_rated_feature_vectors.append(normalized_vector)

    
    ## ALGORITHM FOR CUSTOM BINNING HISTORGRAM ##

    # Initialize a dictionary to store all values for each attribute
    attribute_values = defaultdict(list)

    # Collect values for each attribute across all high-rated songs
    for vector in high_rated_feature_vectors:
        for attr_index, value in enumerate(vector):
            attribute_name = get_attribute_name(attr_index)
            attribute_values[attribute_name].append(value)

    # Determine the most populated range for each attribute
    attribute_ranges = {}
    range_size = 0.2  # Define the size of each range

    for attr, values in attribute_values.items():
        # Filter out values less than or equal to 0.2
        filtered_values = [value for value in values if value > 0.2]

        # Bin values into ranges starting from 0.2
        bins = np.arange(0.2, 1 + range_size, range_size)
        hist, bin_edges = np.histogram(filtered_values, bins=bins)

        # Find the range with the maximum count
        max_count_index = np.argmax(hist)
        common_range = (bin_edges[max_count_index], bin_edges[max_count_index + 1])
        
        attribute_ranges[attr] = common_range

    # Prepare the display message
    display_messages.append("Most common ranges for attributes in your top-rated songs (excluding 0 to 0.2):")
    for attr, common_range in attribute_ranges.items():
        display_messages.append(f"- {attr}: Most Common Range {common_range}")


    # PLOTTING DENSITY PLOT

    # Initialize a dictionary to store all values for each attribute
    attribute_values = defaultdict(list)

    # Collect values for each attribute across all high-rated songs
    for vector in high_rated_feature_vectors:
        for attr_index, value in enumerate(vector):
            attribute_name = get_attribute_name(attr_index)
            if value > 0.2:  # Exclude values between 0.0 and 0.2
                attribute_values[attribute_name].append(value)

    # Define color palettes for each category
    genre_colors = sns.color_palette('Set1', len(genre_score))
    mood_colors = sns.color_palette('Set2', len(mood_score))
    vocal_colors = sns.color_palette('Set3', len(vocal_score))

    
    # Create a combined density plot for each category

    # Plot for Genres
    plt.figure(figsize=(5, 3))
    for (genre, _), color in zip(genre_score.items(), genre_colors):
        sns.kdeplot(attribute_values[genre], label=genre, color=color, fill=True, bw_adjust=0.5)
    plt.title('Density Plots for Genres', fontsize=14)
    plt.xlabel('Attribute Values', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend()
    plt.tight_layout()
    # Save the first plot
    genre_png = io.BytesIO()
    plt.savefig(genre_png, format='png')
    genre_png.seek(0)
    genre_encoded = base64.b64encode(genre_png.getvalue()).decode('utf-8')
    plt.close()

    # Plot for Moods
    plt.figure(figsize=(5, 3))
    for (mood, _), color in zip(mood_score.items(), mood_colors):
        sns.kdeplot(attribute_values[mood], label=mood, color=color, fill=True, bw_adjust=0.5)
    plt.title('Density Plots for Moods', fontsize=14)
    plt.xlabel('Attribute Values', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend()
    plt.tight_layout()
    # Save the second plot
    mood_png = io.BytesIO()
    plt.savefig(mood_png, format='png')
    mood_png.seek(0)
    mood_encoded = base64.b64encode(mood_png.getvalue()).decode('utf-8')
    plt.close()

    # Plot for Vocals
    plt.figure(figsize=(5, 3))
    for (vocal, _), color in zip(vocal_score.items(), vocal_colors):
        sns.kdeplot(attribute_values[vocal], label=vocal, color=color, fill=True, bw_adjust=0.5)
    plt.title('Density Plots for Vocals', fontsize=14)
    plt.xlabel('Attribute Values', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend()
    plt.tight_layout()
    # Save the third plot
    vocal_png = io.BytesIO()
    plt.savefig(vocal_png, format='png')
    vocal_png.seek(0)
    vocal_encoded = base64.b64encode(vocal_png.getvalue()).decode('utf-8')
    plt.close()

    # Pass the encoded images and other necessary information to the template
    return render_template(
        'single_test_results.html', 
        user=user, 
        test=test, 
        genre_score=genre_score, 
        mood_score=mood_score, 
        vocal_score=vocal_score, 
        display_messages=display_messages,
        genre_image=genre_encoded,
        mood_image=mood_encoded,
        vocal_image=vocal_encoded
    )

# @results.route("/test-results/<int:user_id>", methods=['GET', 'POST'])
# @login_required
# def show_user_results():
#     # load all of users previous tests -> might want to add this to user instead

@results.route("/test_history")
@login_required
def test_history():
    tests = Test.query.filter_by(subject=current_user).order_by(Test.id.asc()).all()

    return render_template("test_history.html", tests=tests)