from WebApp import db, create_app
import os
from misc.predict_genre import predict_genre
from misc.predict_mood import predict_mood
from misc.predict_timbre import predict_timbre
import json

# path for predicting genre, mood, timbre
genre_model_path = ""
genre_saved_mfcc = ""
mood_model_path = ""
mood_saved_mfcc = ""
timbre_model_path = ""
timbre_saved_mfcc = ""
test_data_path = ""

app = create_app()

# genre = predict_genre(genre_model_path, test_data_path, genre_saved_mfcc)
# mood = predict_mood(mood_model_path, test_data_path, mood_saved_mfcc)
# timbre = predict_timbre(timbre_model_path, test_data_path, timbre_saved_mfcc)

# Save audio files into DB
with app.app_context():
    db.drop_all()
    db.create_all()
    from WebApp.models import AudioFile
    audio_files_dir = os.path.join(os.getcwd(), 'WebApp', 'static', 'audio')
    for file_name in os.listdir(audio_files_dir):
        file_path = os.path.join(audio_files_dir, file_name)

        # change dict using json.dump
        genre_data = json.dumps({})#json.dumps(genre[file_name])
        mood_data = json.dumps({})#json.dumps(mood[file_name])
        timbre_data = json.dumps({})#json.dumps(timbre[file_name])

        audio_file = AudioFile(audio_name=file_name, file_path=file_path, genre=genre_data, mood=mood_data, vocal=timbre_data)
        db.session.add(audio_file)
    db.session.commit()