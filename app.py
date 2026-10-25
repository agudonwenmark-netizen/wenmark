
from flask import Flask, request, jsonify, render_template
import sqlite3
import requests
from urllib.parse import urlparse

app = Flask(__name__)
DATABASE = "students.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def student_dict(row):
    return dict(row)


# Web interface
@app.route("/")
def index():
    return render_template("index.html")


# READ all local students
@app.route("/api/students", methods=["GET"])
def get_students():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM students ORDER BY student_id DESC"
    ).fetchall()
    conn.close()
    return jsonify([student_dict(row) for row in rows])


# CREATE a student
@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}

    required = ["name", "program", "year", "section"]
    if any(not str(data.get(field, "")).strip() for field in required):
        return jsonify({"error": "Please complete all fields."}), 400

    conn = get_db()
    cursor = conn.execute(
        """INSERT INTO students (name, program, year, section)
           VALUES (?, ?, ?, ?)""",
        tuple(str(data[field]).strip() for field in required)
    )
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Student added successfully.",
        "student_id": student_id
    }), 201


# READ one student
@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    ).fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Student not found."}), 404

    return jsonify(student_dict(row))


# UPDATE a student
@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json(silent=True) or {}
    required = ["name", "program", "year", "section"]

    if any(not str(data.get(field, "")).strip() for field in required):
        return jsonify({"error": "Please complete all fields."}), 400

    conn = get_db()
    cursor = conn.execute(
        """UPDATE students
           SET name = ?, program = ?, year = ?, section = ?
           WHERE student_id = ?""",
        (
            str(data["name"]).strip(),
            str(data["program"]).strip(),
            str(data["year"]).strip(),
            str(data["section"]).strip(),
            student_id
        )
    )
    conn.commit()
    changed = cursor.rowcount
    conn.close()

    if changed == 0:
        return jsonify({"error": "Student not found."}), 404

    return jsonify({"message": "Student updated successfully."})


# DELETE a student
@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_db()
    cursor = conn.execute(
        "DELETE FROM students WHERE student_id = ?",
        (student_id,)
    )
    conn.commit()
    changed = cursor.rowcount
    conn.close()

    if changed == 0:
        return jsonify({"error": "Student not found."}), 404

    return jsonify({"message": "Student deleted successfully."})


# Retrieve classmate records through this Flask server.
# The remote database is read-only from this application.
@app.route("/api/classmate", methods=["GET"])
def get_classmate_records():
    url = request.args.get("url", "").strip()
    parsed = urlparse(url)

    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or not parsed.hostname.endswith(".onrender.com")
        or parsed.username
        or parsed.password
    ):
        return jsonify({
            "error": "Enter your classmate's HTTPS Render API URL."
        }), 400

    if not parsed.path.rstrip("/").endswith("/api/students"):
        return jsonify({
            "error": "URL must end with /api/students."
        }), 400

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        records = response.json()

        if not isinstance(records, list):
            return jsonify({
                "error": "The classmate API did not return a JSON list."
            }), 502

        return jsonify(records)

    except (requests.RequestException, ValueError):
        return jsonify({
            "error": "Unable to retrieve classmate records. Check the URL and try again."
        }), 502


if __name__ == "__main__":
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                program TEXT NOT NULL,
                year TEXT NOT NULL,
                section TEXT NOT NULL
            )
        """)

    app.run(host="0.0.0.0", port=5000, debug=True)
