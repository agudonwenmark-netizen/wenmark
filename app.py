import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# Database connection
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Student API from database
@app.route('/student')
def get_student():
    conn = get_db_connection()

    student = conn.execute(
        'SELECT * FROM students WHERE student_id = ?',
        ('24-00174',)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "student_id": student["student_id"],
        "name": student["name"],
        "program": student["program"],
        "year": student["year"],
        "section": student["section"]
    })


# Greeting API
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')

    return jsonify({
        "message": f"Hello, {name}!"
    })


# Custom course API
@app.route('/course')
def get_course():
    return jsonify({
        "course": "BSIT",
        "description": "Bachelor of Science in Information Technology",
        "year_level": 3,
        "section": "A"
    })


# Get all students
@app.route('/students')
def get_students():
    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()

    conn.close()

    return jsonify([
        dict(student) for student in students
    ])


# Get one student by ID
@app.route('/students/<int:id>')
def get_student_by_id(id):

    conn = get_db_connection()

    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify(dict(student))


# Additional custom database endpoint
# Display students from Section A
@app.route('/students/section/<section>')
def get_students_by_section(section):

    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students WHERE section = ?',
        (section.upper(),)
    ).fetchall()

    conn.close()

    return jsonify([
        dict(student) for student in students
    ])


if __name__ == '__main__':
    app.run(debug=True)