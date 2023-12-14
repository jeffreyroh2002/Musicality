from WebApp import create_app
from WebApp.models import AudioFile, db
import json
import sys

#create app object
app = create_app()

# Assuming you are still within the application context (Musicality)
with app.app_context():
    # Open a text file for writing
    with open('output_6_balanced.txt', 'w') as file:
        sys.stdout = file  # Redirect stdout to the file

        # Print genre information
        audio_files = db.session.query(AudioFile).all()
        for audio_file in audio_files:
            print(f"Audio Name: {audio_file.audio_name}")
            print(f"File Path: {audio_file.file_path}")

            # Check if genre data is present and not a float
            if audio_file.genre and not isinstance(audio_file.genre, float):
                genre_scores = audio_file.genre
                try:
                    genre_data = json.loads(genre_scores)
                except json.JSONDecodeError:
                    print("Error decoding genre_data JSON.")
                    continue

                print("Genre Values:")
                for genre_name, proportion in genre_data.items():
                    print(f"  {genre_name}: {proportion}")
            else:
                print("Genre data is not available or is in an unexpected format.")

            print()  # Add an empty line between entries

        # Print mood information
        for audio_file in audio_files:
            print(f"Audio Name: {audio_file.audio_name}")
            print(f"File Path: {audio_file.file_path}")

            # Check if mood data is present and not a float
            if audio_file.mood and not isinstance(audio_file.mood, float):
                mood_scores = audio_file.mood
                try:
                    mood_data = json.loads(mood_scores)
                except json.JSONDecodeError:
                    print("Error decoding mood_data JSON.")
                    continue

                print("Mood Values:")
                for mood_name, proportion in mood_data.items():
                    print(f"  {mood_name}: {proportion}")
            else:
                print("Mood data is not available or is in an unexpected format.")

            print()  # Add an empty line between entries

        # Print vocal information
        for audio_file in audio_files:
            print(f"Audio Name: {audio_file.audio_name}")
            print(f"File Path: {audio_file.file_path}")
            print(f"Vocal: {audio_file.vocal}")

            # Check if vocal data is present and not a float
            if audio_file.vocal and not isinstance(audio_file.vocal, float):
                vocal_scores = audio_file.vocal
                try:
                    vocal_data = json.loads(vocal_scores)
                except json.JSONDecodeError:
                    print("Error decoding vocal_data JSON.")
                    continue

                print("Vocal Values:")
                for vocal_name, proportion in vocal_data.items():
                    print(f"  {vocal_name}: {proportion}")
            else:
                print("Vocal data is not available or is in an unexpected format.")

            print()  # Add an empty line between entries

        # Reset stdout to the default value
        sys.stdout = sys.__stdout__