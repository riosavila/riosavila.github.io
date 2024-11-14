import sqlite3
conn = sqlite3.connect('grades.db')
cursor = conn.cursor()
cursor.execute('''
                CREATE TABLE IF NOT EXISTS students
                (id INTEGER PRIMARY KEY, 
                 name TEXT, email TEXT)
               ''')
cursor.execute('''
                CREATE TABLE IF NOT EXISTS Quizzes
                (qzid INTEGER PRIMARY KEY, 
                 id INTEGER,
                 grade INTEGER,
                 FOREIGN KEY (id) REFERENCES students(id))
               ''')
cursor.execute('''
                SELECT * FROM students
               ''')
conn.commit()
conn.close()