from WebApp import create_app
from WebApp.models import AudioFile, db
import json


#create app object
app = create_app()

# Assuming you are still within the application context (Musicality)
with app.app_context():

    audio_file = db.session.query(AudioFile).first()
    print(f"Audio Name: {audio_file.audio_name}")
    print(f"File Path: {audio_file.file_path}")
    if audio_file.genre and not isinstance(audio_file.genre, float):
        genre_scores = audio_file.genre
        try:
            genre_data = json.loads(genre_scores)
        except json.JSONDecodeError:
            print("Error decoding genre_data JSON.")

        for genre_name, proportion in genre_data.items():
            print(genre_name)
            print(proportion)
    else:
        print("Genre data is not available or is in an unexpected format.")

    print()  # Add an empty line between entries

    # # Check if genre data is present and not a float
    # if audio_file.genre and not isinstance(audio_file.genre, float):
    #     genre_scores = audio_file.genre
    #     try:
    #         genre_data = json.loads(genre_scores)
    #     except json.JSONDecodeError:
    #         print("Error decoding genre_data JSON.")

    #     print("Genre Values:")
    #     for genre_name, proportion in genre_data.items():
    #         print(f"  {genre_name}: {proportion}")
    # else:
    #     print("Genre data is not available or is in an unexpected format.")

    # print()  # Add an empty line between entries