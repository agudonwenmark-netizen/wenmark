import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
''')

cursor.execute("DELETE FROM students")

students = [
    ('24-00174', 'Wen Mark Agudon', 'BSIT', 3, 'A'),
    ('24-00175', 'Daniel James Rivera', 'BSIT', 3, 'A'),
    ('24-00176', 'Mary Grace Villanueva', 'BSIT', 3, 'B'),
    ('25-00177', 'Adrian Paul Fernandez', 'BSIT', 2, 'B'),
    ('25-00178', 'Rhea Nicole Bautista', 'BSIT', 2, 'A'),
    ('25-00179', 'Francis Carlo Aquino', 'BSIT', 3, 'B'),
    ('24-00180', 'Camille Rose Navarro', 'BSIT', 3, 'A')
]

cursor.executemany('''
INSERT INTO students (student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
''', students)

conn.commit()
conn.close()

print("Database created successfully.")