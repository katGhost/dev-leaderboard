from flask import Blueprint, render_template, session, redirect, url_for, request
from functools import wraps


# set up app blueprint
app_bp = Blueprint('app', __name__)


@app_bp.route('/')
def home():
    return render_template('index.html')


@app_bp.route('/dashboard')
def dashboard():
    if "user" not in session:
        return redirect(url_for('home'))

    user = session["user"]
    return render_template('dashboard.html', user=user)


@app_bp.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')


# TODO: Add Auth0 login/logout routes here
@app_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    # Auth0 Login
    return redirect('/login')


@app_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


# Toggle theme UI
@app_bp.route('/toggle-theme')
def toggle_theme():
    current_theme = session.get("theme", "light")
    new_theme = "dark" if current_theme == "light" else "light"
    session["theme"] = new_theme
    #flash(f"Theme switched to {new_theme}.")
    ref = request.referrer or "/"
    return redirect(ref)
