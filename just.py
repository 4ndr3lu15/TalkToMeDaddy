import sqlite3

conn = sqlite3.connect('audio_database.db')
c = conn.cursor()
# create audio table
c.execute('CREATE TABLE audio (word text, audio_file text)')

# get the name of all files in the audio folder
import os
audio_files = os.listdir('static/audio')

# insert the audio files into the database
for audio_file in audio_files:
    ç = 'static/audio/'
    word = audio_file.split('.')[0]
    c.execute('INSERT INTO audio VALUES (?, ?)', (word, ç + audio_file))

# commit the changes to the database
conn.commit()