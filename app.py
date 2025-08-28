# app.py
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import pandas as pd
import os
from datetime import datetime

# --- Paths ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(CURRENT_DIR, 'dashboard', 'templates')
STATIC_DIR = os.path.join(CURRENT_DIR, 'dashboard', 'static')

# --- Flask App & Login Setup ---
app = Flask(__name__,
            template_folder=TEMPLATE_DIR,
            static_folder=STATIC_DIR)

app.secret_key = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6'  # Change this!

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."

# Simple user class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# In-memory user (for demo)
USERS = {
    'admin': {
        'password': 'admin123',  # Change this!
        'id': 1
    }
}

@login_manager.user_loader
def load_user(user_id):
    for username, user_data in USERS.items():
        if str(user_data['id']) == user_id:
            return User(id=user_id)
    return None

# --- File paths ---
DATA_DIR = 'data'
EVENTS_FILE = os.path.join(DATA_DIR, 'events.csv')
ALERTS_FILE = os.path.join(DATA_DIR, 'alerts.csv')

# --- Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = USERS.get(username)
        if user and user['password'] == password:
            login_user(User(id=user['id']))
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/alerts')
@login_required
def alerts_page():
    if os.path.exists(ALERTS_FILE):
        df = pd.read_csv(ALERTS_FILE, parse_dates=['time'])
        alerts = df.to_dict('records')
    else:
        alerts = []
    return render_template('alerts.html', alerts=alerts)

@app.route('/api/stats')
@login_required
def api_stats():
    if not os.path.exists(EVENTS_FILE):
        return jsonify({"error": "No data available"}), 404

    try:
        df = pd.read_csv(EVENTS_FILE, parse_dates=['timestamp'])
        df['hour'] = df['timestamp'].dt.hour

        total_events = len(df)
        users = df['user'].nunique()
        critical_events = len(df[df['event_id'].isin([4624, 4663, 4664])])

        hourly_logins = df[df['event_id'] == 4624].groupby('hour').size()
        hourly_logins = hourly_logins.reindex(range(24), fill_value=0).tolist()

        non_zero_values = [v for v in hourly_logins if v > 0]
        non_zero_hours = [str(i) for i, v in enumerate(hourly_logins) if v > 0]

        return jsonify({
            "total_events": total_events,
            "unique_users": users,
            "critical_events": critical_events,
            "hourly_logins": non_zero_values,
            "hour_labels": non_zero_hours
        })

    except Exception as e:
        print(f"Error in /api/stats: {e}")
        return jsonify({"error": "Failed to process data"}), 500

@app.route('/live')
@login_required
def live_feed():
    return render_template('live.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)