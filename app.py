from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("school.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table automatically
conn = get_db()

conn.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT,
class_name TEXT,
subject TEXT,
marks INTEGER
)
""")

conn.commit()
conn.close()

@app.route("/")
def index():

    name = request.args.get("name","")
    class_name = request.args.get("class_name","")

    conn = get_db()

    query = "SELECT * FROM students WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE ?"
        params.append("%"+name+"%")

    if class_name:
        query += " AND class_name LIKE ?"
        params.append("%"+class_name+"%")

    students = conn.execute(query, params).fetchall()

    conn.close()

    return render_template("index.html", students=students)

@app.route("/add", methods=["GET","POST"])
def add():

    if request.method == "POST":

        conn = get_db()

        conn.execute("""
        INSERT INTO students
        (name,email,password,class_name,subject,marks)
        VALUES (?,?,?,?,?,?)
        """,
        (
            request.form["name"],
            request.form["email"],
            request.form["password"],
            request.form["class_name"],
            request.form["subject"],
            request.form["marks"]
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")

@app.route("/delete/<int:id>")
def delete(id):

    conn = get_db()

    conn.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):

    conn = get_db()

    if request.method == "POST":

        conn.execute("""
        UPDATE students
        SET name=?,email=?,class_name=?,subject=?,marks=?
        WHERE id=?
        """,
        (
            request.form["name"],
            request.form["email"],
            request.form["class_name"],
            request.form["subject"],
            request.form["marks"],
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template("edit.html", student=student)

if __name__ == "__main__":
    app.run(debug=True)