import sqlite3

con = sqlite3.connect('register_LI.db')
cursor = con.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Universal_commands (
id INTEGER PRIMARY KEY,
model TEXT NOT NULL,
command TEXT NOT NULL
)
''')


con.commit()
con.close()
