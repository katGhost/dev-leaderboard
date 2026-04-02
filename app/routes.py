from functools import wraps
import requests
from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.oauth import oauth
from app.config import Config
from app.extensions import db
from authlib.jose import jwt
from app.models import User


app_bp = Blueprint('app', __name__)


@app_bp.route('/')
def home():
    return render_template('index.html')


@app_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('app.home'))

    user = User.query.get(session.get('user_id'))
    return render_template('dashboard.html', user=user)


@app_bp.route('/leaderboard')
def leaderboard():
    if 'user_id' not in session:
        return redirect(url_for('app.home'))

    # fetch all users who have connected github
    users_with_github = User.query.filter(
        User.github_token.isnot(None)
    ).all()

    leaderboard_data = []
    for u in users_with_github:
        from app.services.github_service import GithubService
        github = GithubService(u.github_token)
        score = github.get_weekly_contributions(u.github_username)
        leaderboard_data.append({
            'name': u.name,
            'nickname': u.nickname,
            'picture': u.picture,
            'github_username': u.github_username,
            'score': score
        })

    leaderboard_data.sort(key=lambda x: x['score'], reverse=True)

    return render_template('leaderboard.html', users=leaderboard_data)


@app_bp.route('/login', methods=['GET', 'POST'])
def login():
    redirect_uri = url_for('app.callback', _external=True)
    return oauth.auth0.authorize_redirect(redirect_uri)


@app_bp.route('/callback', methods=['GET', 'POST'])
def callback():
    token = oauth.auth0.authorize_access_token()
    session['auth_token'] = token

    # print("FULL TOKEN:", token)
    # print("USERINFO FROM TOKEN:", token.get('userinfo'))

    resp = oauth.auth0.get(
        f'https://{Config.AUTH0_DOMAIN}/userinfo',
        token=token
    )
    user_info = resp.json()
    print("USERINFO:", user_info)

    # upsert user into DB
    auth0_id = user_info.get('sub')
    user = User.query.filter_by(auth0_id=auth0_id).first()

    # if user in the db ->
    if not user:
        # first time login, create user
        user = User(
            auth0_id=auth0_id,
            name=user_info.get('name'),
            email=user_info.get('email'),
            picture=user_info.get('picture'),
            nickname=user_info.get('nickname'),
        )
        db.session.add(user)
    else:
        # returning user, update their info
        user.name = user_info.get('name')
        user.email = user_info.get('email')
        user.picture = user_info.get('picture')
        user.nickname = user_info.get('nickname')
    
    db.session.commit()

    # storing only the db user_id in session
    session['user_id'] = user.id
    print('SESSION_USER_ID: ', session.get('user_id'))

    return redirect(url_for('app.profile'))


@app_bp.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('app.home'))

    user = User.query.get(session.get('user_id'))
    # print(f'USER FROM DB: ', user)
    # do something about the user info display and storage
    return render_template('profile.html', user=user)


@app_bp.route('/connect/github')
def github_login():
    # only Auth0 logged-in users can connect to github
    # Good for token vault -> Auth0 needs a logged-in user identity to associate the stored GitHub token against
    if 'user_id' not in session:
        return redirect(url_for('app.home'))
    
    redirect_uri = url_for('app.github_callback', _external=True)
    print('GITHUB REDIRECT: ', redirect_uri)
    return oauth.github.authorize_redirect(redirect_uri)


@app_bp.route('/github/callback')
def github_callback():
    print('REDIRECT URI HIT!')
    if 'user_id' not in session:
        return redirect(url_for('app.home'))

    token = oauth.github.authorize_access_token()
    print(f'FULL GITHUB TOKEN: ', token)
    github_token = token['access_token']

    # fetch github username
    headers = {'Authorization': f'Bearer {github_token}'}
    resp = requests.get('https://api.github.com/user', headers=headers)
    github_user = resp.json()

    # save token sadn user to db
    user = User.query.get(session.get('user_id'))
    if not user:
        return redirect(url_for('app.home'))

    print(f'Github User: ', user)
    user.github_token = github_token
    user.github_username = github_user.get('login')
    db.session.commit()

    return redirect(url_for('app.dashboard'))


@app_bp.route('/logout')
def logout():
    session.pop('user_info', None)  # fixed key
    session.pop('auth_token', None)
    session.pop('github_token', None)
    session.clear()
    return redirect(url_for('app.home'))  # fixed blueprint prefix