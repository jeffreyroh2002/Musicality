#Script that takes in 3 train models, predicts each attribute for song, 
#and save information into a json file that stores key and value

import json
import numpy as np
from tensorflow import keras
import os

genre_model = os.path.join(os.getcwd(), 'WebApp', 'python_scripts', 'pred_genre', 'saved_model')
mood_model = os.path.join(os.getcwd(), 'WebApp', 'python_scripts', 'pred_mood', 'saved_model')
vocal_model = os.path.join(os.getcwd(), 'WebApp', 'python_scripts', 'pred_vocal', 'saved_model')

audio_mfcc_path = ""





audio_files_dir = os.path.join(os.getcwd(), 'WebApp', 'static', 'audio_full_mix')
for file_name in os.listdir(audio_files_dir):
    