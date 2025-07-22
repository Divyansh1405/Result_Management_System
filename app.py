from flask import Flask, render_template, request, redirect, url_for, session, send_file
import mysql.connector
from utils.pdf_generator import generate_pdf
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Config
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",  # change this
    database="result_db"
)
cursor = db.cursor()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        admin = request.form['username']
        password = request.form['password']
        if admin == "admin" and password == "admin123":
            session['admin'] = admin
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect('/login')
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    return render_template('dashboard.html', students=data)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        roll = request.form['roll']
        name = request.form['name']
        math = request.form['math']
        sci = request.form['science']
        eng = request.form['english']
        cursor.execute("INSERT INTO students VALUES (%s, %s, %s, %s, %s)", (roll, name, math, sci, eng))
        db.commit()
        return redirect('/dashboard')
    return render_template('add_student.html')

@app.route('/update/<roll>', methods=['GET', 'POST'])
def update_student(roll):
    if request.method == 'POST':
        name = request.form['name']
        math = request.form['math']
        sci = request.form['science']
        eng = request.form['english']
        cursor.execute("UPDATE students SET name=%s, math=%s, science=%s, english=%s WHERE roll_no=%s",
                       (name, math, sci, eng, roll))
        db.commit()
        return redirect('/dashboard')
    cursor.execute("SELECT * FROM students WHERE roll_no=%s", (roll,))
    student = cursor.fetchone()
    return render_template('update_student.html', student=student)

@app.route('/delete/<roll>')
def delete_student(roll):
    cursor.execute("DELETE FROM students WHERE roll_no=%s", (roll,))
    db.commit()
    return redirect('/dashboard')

@app.route('/result/<roll>')
def view_result(roll):
    cursor.execute("SELECT * FROM students WHERE roll_no=%s", (roll,))
    student = cursor.fetchone()
    if student:
        return render_template('student_result.html', student=student)
    return "Student Not Found"

@app.route('/download/<roll>')
def download_pdf(roll):
    cursor.execute("SELECT * FROM students WHERE roll_no=%s", (roll,))
    student = cursor.fetchone()
    path = generate_pdf(student)
    return send_file(path, as_attachment=True)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
