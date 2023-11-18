import sys
import os
from pydub import AudioSegment

def split_wav_into_segments(input_directory, output_directory, txt_file, segment_length_ms=60000):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    with open(txt_file, "r") as file:
        content = file.readline()
        while content != "":
            content = content.strip()  # remove \n
            data = content.split(",")
            song_name = data[0]
            start_time = data[1]
            end_time = start_time + segment_length_ms
            
            # Load the input WAV file
            input_path = os.path.join(input_directory, song_name)
            audio = AudioSegment.from_wav(input_path)

            segment = audio[start_time:end_time]

            # Define the output file name
            output_file = os.path.join(output_directory, song_name)

            # Export the segment as a new WAV file
            segment.export(output_file, format="wav")
            
            content = file.readline()


    for input_file in input_files:
        input_path = os.path.join(input_directory, input_file)

        

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py input_directory output_directory")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    txt_file_path = sys.argv[3]

    split_wav_into_segments(input_directory, output_directory, txt_file_path)

