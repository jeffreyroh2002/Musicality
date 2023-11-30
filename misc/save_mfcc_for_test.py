import json
import os
import math
import librosa

DATASET_PATH = "../EpidemicSoundRaw/audio_vocals_split"
JSON_FILE_NAME = "../WebApp/static/mfccs/vocals_mfcc.json"
JSON_PATH = JSON_FILE_NAME

SAMPLE_RATE = 22050

def save_mfcc(dataset_path, json_path, n_mfcc=13, n_fft=2048, hop_length=512):

    # data dictionary
    data = {
        "mapping": [],
        "mfcc": [],
        "labels": [],
        "filenames": []  # Store the file names
    }


    for file_name in os.listdir(dataset_path):

        file_path = os.path.join(dataset_path, file_name)
        signal, sr = librosa.load(file_path, sr=SAMPLE_RATE)
        
        # calculate the audio file length, and fit the expected_num_mfcc_vectors_per_segment value
        duration = int(signal.shape[0]/float(sr))  # measured in seconds for GTZAN Dataset
        samples_per_track = SAMPLE_RATE * duration
        num_segments = int(duration / 3)

        num_samples_per_segment = int(samples_per_track / num_segments)

        # need the number of vectors for mfcc extraction to be equal for each segment
        expected_num_mfcc_vectors_per_segment = math.ceil(num_samples_per_segment / hop_length)

        # process segments extracting mfcc and storing data
        for s in range(num_segments):
            start_sample = num_samples_per_segment * s
            finish_sample = start_sample + num_samples_per_segment

            mfcc = librosa.feature.mfcc(y=signal[start_sample:finish_sample],
                                            sr=sr,
                                            n_fft=n_fft,
                                            n_mfcc=n_mfcc,
                                            hop_length=hop_length)
            mfcc = mfcc.T

            # store mfcc for a segment if it has the expected length
            if len(mfcc) == expected_num_mfcc_vectors_per_segment:
                data["mfcc"].append(mfcc.tolist())  # convert numpy array to list
                data["labels"].append(0)
                data["filenames"].append(file_name)  # fixed this line
                print("{}, segment:{}".format(file_name, s))

    with open(json_path, "w") as fp:
        json.dump(data, fp, indent=4)


if __name__ == "__main__":
    save_mfcc(DATASET_PATH, JSON_PATH)