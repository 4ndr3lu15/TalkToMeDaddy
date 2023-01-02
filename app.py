from flask import Flask, render_template, request
import sqlite3
from pydub import AudioSegment

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the text input from the form
        input_text = request.form['input_text']

        # Split the input text into words
        words = input_text.split()

        # Connect to the database
        conn = sqlite3.connect('audio_database.db')
        c = conn.cursor()

        available_words = list(c.execute('SELECT word FROM audio')) 
        available_words = [word[0] for word in available_words]
        
        # Check if all the words are available
        for word in words:
            if word not in available_words:
                return render_template('bad_request.html')

        # Initialize an empty list to store the audio segments
        audio_segments = []

        # Query the database for the audio files for each word
        for word in words:
            c.execute('SELECT audio_file FROM audio WHERE word=?', (word,))
            audio_file = c.fetchone()
            if audio_file:
                # Load the audio file using pydub
                audio_segment = AudioSegment.from_file(audio_file[0], format='mp3')
                audio_segments.append(audio_segment)

        # Concatenate the audio segments
        concatenated_audio = audio_segments[0]
        for audio_segment in audio_segments[1:]:
            concatenated_audio += audio_segment

        # Export the concatenated audio file
        concatenated_audio.export('static/output/concatenated_audio.mp3', format='mp3')

        # Close the database connection
        conn.close()

        # Render the results template with the list of audio files
        return render_template('results.html', audio_file='static/output/concatenated_audio.mp3')
    else:
        # Render the index template
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)