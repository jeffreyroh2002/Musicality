import re

def process_genre_data(text_data):
    # Regular expression pattern to extract data
    pattern = re.compile(
        r'Audio Name: (?P<MusicName>.+\.wav_\d+\.wav)\nFile Path: (?P<FilePath>.+)\nGenre Values:\n(?:\s{2}(?P<Genre>[^\n]+):\s(?P<Value>[\d.]+)\n?)+'
    )

    # Find all matches in the text data
    matches = pattern.finditer(text_data)

    # Create a dictionary to store genre information for each music
    music_genre_data = {}

    # Extract data from matches
    for match in matches:
        music_name = match.group('MusicName')
        genre_values = {
            genre.group('Genre'): float(genre.group('Value'))
            for genre in re.finditer(r'(?P<Genre>[^\n]+):\s(?P<Value>[\d.]+)\n?', match.group(0))
        }
        music_genre_data[music_name] = genre_values

    return music_genre_data

def analyze_genre_data(music_genre_data):
    # Create dictionaries to store genre counts and percentages
    genre_count = {genre: 0 for genre in music_genre_data[next(iter(music_genre_data))]}
    genre_percentage_sum = {genre: 0.0 for genre in music_genre_data[next(iter(music_genre_data))]}

    # Analyze genre data
    for genre_values in music_genre_data.values():
        for genre, value in genre_values.items():
            if value != 0:
                genre_count[genre] += 1
                genre_percentage_sum[genre] += value

    return genre_count, genre_percentage_sum

def write_analysis_results(genre_count, genre_percentage_sum, output_file_path):
    # Write analysis results to a text file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Genre Analysis Results\n\n")
        output_file.write("{:<20} {:<20} {:<20}\n".format("Genre", "Nonzero Count", "Total Percentage"))

        # Write genre analysis results
        for genre in genre_count:
            output_file.write("{:<20} {:<20} {:<20}\n".format(genre, genre_count[genre], genre_percentage_sum[genre]))

# Read text data from the file
with open('final.txt', 'r', encoding='utf-8') as file:
    text_data = file.read()

# Process genre data from the text
music_genre_data = process_genre_data(text_data)

# Analyze genre data
genre_count, genre_percentage_sum = analyze_genre_data(music_genre_data)

# Write analysis results to a text file
write_analysis_results(genre_count, genre_percentage_sum, 'genre_analysis_results.txt')

print("Genre analysis results have been saved to genre_analysis_results.txt.")
