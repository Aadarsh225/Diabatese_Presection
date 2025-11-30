from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import numpy as np
import joblib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ---------------------------
# DATABASE INITIAL SETUP
# ---------------------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # History table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            result TEXT,
            pregnancies REAL,
            glucose REAL,
            bp REAL,
            skin REAL,
            insulin REAL,
            bmi REAL,
            dpf REAL,
            age REAL,
            date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------------------
# LOAD MODEL
# ---------------------------
model = joblib.load("model/diabetes_model.pkl")
scaler = joblib.load("model/scaler.pkl")

# ---------------------------
# ROUTES
# ---------------------------
@app.route('/')
def home():
    if "user_id" in session:
        return redirect('/index')
    return redirect('/login')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if "user_id" not in session:
        return redirect('/login')

    if request.method == 'POST':
        pregnancies = float(request.form['pregnancies'])
        glucose = float(request.form['glucose'])
        bp = float(request.form['bp'])
        skin = float(request.form['skin'])
        insulin = float(request.form['insulin'])
        bmi = float(request.form['bmi'])
        dpf = float(request.form['dpf'])
        age = float(request.form['age'])

        input_data = np.array([[pregnancies, glucose, bp, skin, insulin, bmi, dpf, age]])
        scaled_data = scaler.transform(input_data)
        prediction = model.predict(scaled_data)[0]
        result = "Diabetic" if prediction == 1 else "Non-Diabetic"

        # Save to history
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO history 
            (user_id, result, pregnancies, glucose, bp, skin, insulin, bmi, dpf, age, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (session['user_id'], result, pregnancies, glucose, bp, skin, insulin, bmi, dpf, age, datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
        conn.close()

        return render_template("result.html", result=result, pregnancies=pregnancies, glucose=glucose, bp=bp, skin=skin, insulin=insulin, bmi=bmi, dpf=dpf, age=age)

    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            flash("Account created! Login now.", "success")
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash("Username already exists!", "danger")
        conn.close()

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = username
            return redirect('/index')
        else:
            flash("Invalid login!", "danger")

    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/login')

    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row  # Important: access columns by name
    cursor = conn.cursor()
    cursor.execute("""
        SELECT result, pregnancies, glucose, bp, skin, insulin, bmi, dpf, age, date 
        FROM history WHERE user_id=? ORDER BY date DESC
    """, (session['user_id'],))
    records = cursor.fetchall()
    conn.close()

    return render_template("dashboard.html", username=session['username'], history=records)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)
