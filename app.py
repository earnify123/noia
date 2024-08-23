from flask import Flask, render_template, redirect, url_for, session, request
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    if 'points' not in session:
        session['points'] = 0
    return render_template('index.html', points=session['points'])

@app.route('/task')
def task():
    return render_template('task.html')

@app.route('/redirect_to_external', methods=['POST'])
def redirect_to_external():
    session['task_start_time'] = time.time()
    return redirect("https://www.google.com")

@app.route('/complete_task')
def complete_task():
    if 'task_start_time' in session:
        elapsed_time = time.time() - session['task_start_time']
        if elapsed_time >= 120:  # 120 seconds or 2 minutes
            session['points'] += 100
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    
