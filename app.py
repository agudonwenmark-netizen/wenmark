from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def home():
    return "hello Wen Mark Agudon!"


@app.route('/greet')
def get_student():
    return jsonify({
        "student_id": "24-00174",
        "name": "Wen Mark Agudon",
        "program": "BSIT",
        "year": 3,
        "section": "Hamilton",
        "email": "agudonwenmark@isufst.edu.ph",
        "skills": [
            "Python",
            "Java",
            "C++"
        ]
    })


@app.route('/course')
def get_course():
    return jsonify({
        "course_code": "IT3120",
        "course_title": "System Integration",
        "instructor": "Dr. Rene Arduo",
        "semester": "First Semester",
        "academic_year": "2026-2027"
    })


@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')

    return jsonify({
        "message": f"Hello, {name}!"
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
