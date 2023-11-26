from WebApp import db, create_app
import os
from WebApp.python_scripts.predict_genre import predict_genre
from WebApp.python_scripts.predict_mood import predict_mood
from WebApp.python_scripts.predict_timbre import predict_timbre
import json

# path for predicting genre, mood, timbre


genre_saved_mfcc = os.path.join(os.getcwd(), 'WebApp', 'static', 'mfccs', 'full_mix_mfcc.json')
mood_saved_mfcc = os.path.join(os.getcwd(), 'WebApp', 'static', 'mfccs', 'instrumental_mfcc.json')
timbre_saved_mfcc = os.path.join(os.getcwd(), 'WebApp', 'static', 'mfccs', 'vocal_mfcc.json')

genre_model_path = os.path.join(os.getcwd(), 'WebApp', 'python_scripts', 'pred_genre', 'saved_model')
mood_model_path = os.path.join(os.getcwd(), 'WebApp', 'python_scripts', 'pred_mood', 'saved_model')
timbre_model_path = os.path.join(os.getcwd(), 'WebApp', 'python_scripts', 'pred_vocal', 'saved_model')

app = create_app()

# Save audio files into DB
with app.app_context():
    db.drop_all()
    db.create_all()
    from WebApp.models import AudioFile

    full_mix_dir = os.path.join(os.getcwd(), 'WebApp', 'static', 'audio_data', 'audio_full_mix_split')
    instrumentals_dir = os.path.join(os.getcwd(), 'WebApp', 'static', 'audio_data', 'audio_instrumental_split')
    vocals_dir = os.path.join(os.getcwd(), 'WebApp', 'static', 'audio_data', 'audio_vocals_split')

    # Iterate through the full mix directory
    for full_mix_file_name in os.listdir(full_mix_dir):
        full_mix_file_path = os.path.join(full_mix_dir, full_mix_file_name)
        
        # Extract the common prefix (first 8 characters) from the full mix file name
        common_prefix = full_mix_file_name[:8]

        # Determine the corresponding instrumental and vocal file names
        instrumental_file_name = common_prefix + "_instrumental.wav"
        vocal_file_name = common_prefix + "_vocal.wav"

        # Generate file paths for instrumental and vocal files
        instrumental_file_path = os.path.join(instrumentals_dir, instrumental_file_name)
        vocal_file_path = os.path.join(vocals_dir, vocal_file_name)

        # Predict and save genre, mood, and timbre data
        genre_data = predict_genre(genre_model_path, genre_saved_mfcc)

        """
        mood_data = predict_mood(mood_model_path, mood_saved_mfcc)

        # Check if the vocal file exists
        if os.path.exists(vocal_file_path):
            timbre_data = predict_timbre(timbre_model_path, timbre_saved_mfcc)
        else:
            # Set the vocal element to "Voiceless" if the vocal file doesn't exist
            timbre_data = {"vocal_element": "Voiceless"}
        """

        # Convert data to JSON format
        genre_data_json = json.dumps(genre_data)
        #mood_data_json = json.dumps(mood_data)
        #timbre_data_json = json.dumps(timbre_data)

        # Create an instance of AudioFile and add it to the database session
        audio_file = AudioFile(
            audio_name=full_mix_file_name,
            file_path=full_mix_file_path,
            genre=genre_data_json,
            #mood=mood_data_json,
            #vocal=timbre_data_json
        )
        db.session.add(audio_file)

    # Commit the changes to the database
    db.session.commit()
