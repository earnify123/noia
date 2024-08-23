from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, auth

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/verify', methods=['POST'])
def verify():
    phone_number = request.form.get('phone_number')
    session['phone_number'] = phone_number
    # Normally, send OTP to phone_number using Firebase here
    return render_template('otp.html')

@app.route('/login', methods=['POST'])
def login():
    otp_code = request.form.get('otp_code')
    phone_number = session.get('phone_number')
    
    # Verify the OTP code with Firebase (simulate for now)
    # In a real implementation, you would verify with Firebase's API
    try:
        # Simulate OTP verification (replace this with real Firebase OTP verification)
        if otp_code == '123456':  # For demonstration purposes
            user = auth.get_user_by_phone_number(phone_number)
            session['user_id'] = user.uid
            return f"Welcome {phone_number}, you have successfully logged in!"
        else:
            return "Invalid OTP code!"
    except auth.UserNotFoundError:
        return "User not found. Please try again!"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
