from WebApp import db, create_app
import os

app = create_app()

app.app_context().push()

# Save audio files into DB
with app.app_context():
    from WebApp.models import AudioFile
    audio_files_dir = os.path.join(os.getcwd(), 'WebApp', 'static', 'audio')
    for file_name in os.listdir(audio_files_dir):
        file_path = os.path.join(audio_files_dir, file_name)
        audio_file = AudioFile(audio_name=file_name, file_path=file_path, genre="None", mood="None", vocal="None")
        db.session.add(audio_file)
    db.session.commit()