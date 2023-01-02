import sqlite3

conn = sqlite3.connect('audio_database.db')
c = conn.cursor()

print(list(c.execute('SELECT word FROM audio')))