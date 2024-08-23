from flask import Flask, render_template, request, redirect, url_for, session, flash
import firebase_admin
from firebase_admin import credentials, auth

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a real secret key

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/do_register', methods=['POST'])
def do_register():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = auth.create_user(email=email, password=password)
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('register'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = auth.get_user_by_email(email)
        # Simulate password check for demonstration purposes
        # In practice, Firebase handles this for you on the client side
        # Firebase's admin SDK doesn't support password verification directly
        # You would need to verify passwords on the client side or use Firebase client SDK
        session['user_id'] = user.uid
        return redirect(url_for('welcome'))
    except auth.UserNotFoundError:
        flash('Invalid email or password.', 'error')
        return redirect(url_for('index'))

@app.route('/welcome')
def welcome():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))
    
    user = auth.get_user(user_id)
    return render_template('welcome.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    
