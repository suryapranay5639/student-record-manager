import sqlite3
from typing import List, Dict

DB_PATH = "students.db"

def init_db() -> None:
    """Create the students table if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                course TEXT NOT NULL
            )
        """)

def add_student(name: str, age: int, course: str) -> int:
    """Add a student and return the new row id."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)", (name, age, course))
        return cur.lastrowid

def view_students() -> List[Dict]:
    """Return a list of students as dictionaries."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.execute("SELECT id, name, age, course FROM students ORDER BY id")
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def update_student(student_id: int, name: str, age: int, course: str) -> int:
    """Update a student; returns number of affected rows."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("UPDATE students SET name=?, age=?, course=? WHERE id=?", (name, age, course, student_id))
        return cur.rowcount

def delete_student(student_id: int) -> int:
    """Delete a student; returns number of affected rows."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("DELETE FROM students WHERE id=?", (student_id,))
        return cur.rowcount

# Ensure DB/table exists when module is imported
init_db()
