from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from firebase_admin import credentials, auth, initialize_app
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase_key.json")
initialize_app(cred)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    points = db.Column(db.Integer, default=0)
    referral_code = db.Column(db.String(120), unique=True)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Register user using Firebase Authentication
        try:
            user = auth.create_user(email=email, password=password)
            # Add user to local database
            new_user = User(email=user.email)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return "Registration failed"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.get_user_by_email(email)
            session['user_id'] = user.uid
            return redirect(url_for('tasks'))
        except:
            return "Login failed"
    return render_template('login.html')

@app.route('/tasks')
def tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        user = User.query.filter_by(id=session['user_id']).first()
        user.points += task.points
        db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.points.desc()).limit(10).all()
    return render_template('leaderboard.html', users=users)

@app.route('/referral')
def referral():
    user = User.query.filter_by(id=session['user_id']).first()
    referral_link = url_for('register', _external=True) + '?ref=' + user.referral_code
    return render_template('referral.html', referral_link=referral_link)

@app.route('/profile')
def profile():
    user = User.query.filter_by(id=session['user_id']).first()
    return render_template('profile.html', user=user)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        try:
            # Send password reset email via Firebase
            auth.send_password_reset_email(email)
            flash("Password reset email sent!", "success")
            return redirect(url_for('login'))
        except:
            flash("Failed to send password reset email", "danger")
    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
            
