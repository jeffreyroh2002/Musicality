from WebApp import create_app
from WebApp.models import AudioFile, db
import json


#create app object
app = create_app()

# Assuming you are still within the application context (Musicality)
with app.app_context():
    # Query all AudioFile records
    # audio_files = db.session.query(AudioFile).all()
    audio_file = db.session.query(AudioFile).first()

    # print(f"Audio Name: {audio_file.audio_name}")
    # print(f"File Path: {audio_file.file_path}")
    # print(f"Genre: {audio_file.genre}")
    # print(f"Mood: {audio_file.mood}")
    # print(f"Vocal: {audio_file.vocal}")
    # print("\n")

    genre_scores = audio_file.genre
    genre_data = json.loads(genre_scores)

    for audio_name, genre_values in genre_data.items():
        print(f"Audio Name: {audio_name}")
        print("Genre Values:")
        for genre, proportion in genre_values.items():
            print(f"  {genre}: {proportion}")

        print()  # Add an empty line between entries