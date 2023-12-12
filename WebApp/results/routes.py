import json
from flask import render_template, redirect, url_for, Blueprint, flash, abort
from flask_login import current_user, login_required
from WebApp.models import db, Test, UserAnswer, AudioFile
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

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
    attributes = ['Blues', 'Ballad', 'Orchestral', 'Country', 'Electronic', 'HipHop', 'Jazz', 'Metal', 
                  'Pop', 'Reggae', 'Rock', 'RB_Soul', 
                  'Angry', 'Bright', 'Melancholic', 'Relaxed', 
                  'Smooth', 'Dreamy', 'Raspy', 'Voiceless']
    
    # Return the attribute name corresponding to the given index
    return attributes[index]

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
        mood_rating = answer.mood_rating
        vocal_timbre_rating = answer.vocal_timbre_rating

        # store highly rated songs into high_rated songs list
        if (overall_rating >= 2):
            high_rated_songs.append(answer.audio_id)

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
                vocal_weighted[vocal_name] = proportion * vocal_timbre_rating
            
            for vocal in vocal_weighted:
                vocal_score[vocal] += vocal_weighted[vocal]
        else:
            print("Vocal data is not available or is in an unexpected format.")
        
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
        
    
    print(high_rated_feature_vectors)

    # Create an empty list to store the similarities
    similarity_scores = []

    # Iterate over each pair of feature vectors
    for i in range(len(high_rated_feature_vectors)):
        for j in range(i + 1, len(high_rated_feature_vectors)):
            # Calculate cosine similarity
            similarity = cosine_similarity([high_rated_feature_vectors[i]], [high_rated_feature_vectors[j]])[0][0]
            
            # Store the similarity score with song indices (or any other identifier you have)
            similarity_scores.append(((i, j), similarity))

    # Print or process the similarity scores as needed
    for pair, score in similarity_scores:
        print(f"Similarity between songs {pair[0]} and {pair[1]}: {score}")
    
    # Sort the similarity scores in descending order
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Set a threshold for high similarity (e.g., 0.7)
    high_similarity_threshold = 0.6

    # Filter out song pairs with high similarity
    high_similarity_pairs = [pair for pair, score in sorted_scores if score > high_similarity_threshold]

    # Analyze the feature vectors of these song pairs

    # Changed the following code to average attribute value between the two similar vectors

    attribute_averages = {}
    for i, j in high_similarity_pairs:
        for attr_index in range(len(high_rated_feature_vectors[i])):
            attribute_value_i = high_rated_feature_vectors[i][attr_index]
            attribute_value_j = high_rated_feature_vectors[j][attr_index]

            # Check if the attribute is significant in either of the vectors
            if attribute_value_i > 0 or attribute_value_j > 0:
                attribute_name = get_attribute_name(attr_index)
                average_value = (attribute_value_i + attribute_value_j) / 2
                attribute_averages[attribute_name] = attribute_averages.get(attribute_name, 0) + average_value

    # Sort the attributes by their cumulative average values
    sorted_attribute_averages = sorted(attribute_averages.items(), key=lambda x: x[1], reverse=True)

    # Interpret and present the findings
    print("Your top music preferences with their average values are characterized by:")
    for attr, average_value in sorted_attribute_averages:
        print(f"- {attr}: Average Value {average_value}")

    #currently printing everything, but preferably average them? and display on template
        
    return render_template('single_test_results.html', user=user, test=test, genre_score=genre_score, mood_score=mood_score, vocal_score=vocal_score)

# @results.route("/test-results/<int:user_id>", methods=['GET', 'POST'])
# @login_required
# def show_user_results():
#     # load all of users previous tests -> might want to add this to user instead

@results.route("/test_history")
@login_required
def test_history():
    tests = Test.query.filter_by(subject=current_user).order_by(Test.id.asc()).all()

    return render_template("test_history.html", tests=tests)