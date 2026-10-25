
import sqlite3

DATABASE = "students.db"


def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            program TEXT NOT NULL,
            year TEXT NOT NULL,
            section TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")


if __name__ == "__main__":
    init_db()
