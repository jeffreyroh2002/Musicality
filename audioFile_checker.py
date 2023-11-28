from WebApp import create_app
from WebApp.models import AudioFile, db
import json


#create app object
app = create_app()

# Assuming you are still within the application context (Musicality)
with app.app_context():

    audio_files = db.session.query(AudioFile).all()

    for audio_file in audio_files:
        print(f"Audio Name: {audio_file.audio_name}")
        print(f"File Path: {audio_file.file_path}")

        # Check if vocal data is present and not a float
        if audio_file.vocal and not isinstance(audio_file.vocal, float):
            vocal_scores = audio_file.vocal
            try:
                vocal_data = json.loads(vocal_scores)
            except json.JSONDecodeError:
                print("Error decoding vocal_data JSON.")
                continue

            print("vocal Values:")
            for vocal_name, proportion in vocal_data.items():
                print(f"  {vocal_name}: {proportion}")
        else:
            print("vocal data is not available or is in an unexpected format.")

        print()  # Add an empty line between entries

    audio_files = db.session.query(AudioFile).all()

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

            print("mood Values:")
            for mood_name, proportion in mood_data.items():
                print(f"  {mood_name}: {proportion}")
        else:
            print("mood data is not available or is in an unexpected format.")

        print()  # Add an empty line between entries

    audio_files = db.session.query(AudioFile).all()

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

            print("vocal Values:")
            for vocal_name, proportion in vocal_data.items():
                print(f"  {vocal_name}: {proportion}")
        else:
            print("vocal data is not available or is in an unexpected format.")

        print()  # Add an empty line between entries
