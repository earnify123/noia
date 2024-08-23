from flask import Flask, render_template, redirect, url_for, request
import time

app = Flask(__name__)

@app.route('/')
def index():
    # Check if the reward parameter is set in the URL
    reward = request.args.get('reward', 'false')
    return render_template('index.html', reward=reward)

@app.route('/reward')
def reward_page():
    return render_template('reward_page.html')

@app.route('/claim_reward')
def claim_reward():
    # Simulate waiting for 120 seconds
    time.sleep(120)
    # After 120 seconds, redirect back to the main page with the reward flag
    return redirect(url_for('index', reward='true'))

if __name__ == '__main__':
    app.run(debug=True)
