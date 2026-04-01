from functools import wraps
from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.oauth import oauth



# set up app blueprint
app_bp = Blueprint('app', __name__)


@app_bp.route('/')
def home():
    return render_template('index.html')


@app_bp.route('/dashboard')
def dashboard():
    if "user_info" not in session:
        return redirect(url_for('home'))

    user = session["user_info"]
    return render_template('dashboard.html', user=user)


@app_bp.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')


"""
    OAuth login
"""
@app_bp.route('/login', methods=['GET', 'POST'])
def login():
    redirect_uri = url_for('app.callback', _external=True)
    return oauth.auth0.authorize_redirect(redirect_uri)
    # return jsonify({'message': 'No OAuth implemented yet'})

@app_bp.route('/callback')
def callback():
    # retreiving and storing access_token, in session
    token = oauth.auth0.authorize_access_token()

    # store token and currently in session user info?
    session['auth_token'] = token
    user_info = oauth.auth0.get('userinfo').json()

    # store user info
    session['user_info'] = user_info

    # later for session persistence -> store access_token in db

    # redirect user to profile or dashboard
    return redirect(url_for('profile'))


@app_bp.route('/profile')
def profile():
    # Check if user is logged in
    if 'user_info' not in session:
        return redirect(url_for('app.home'))  # If not logged in, redirect to login

    user_info = session['user_info']
    return jsonify(user_info)

""" 
    Github
"""
@app_bp.route('/connect/github')
def github_login():
    return oauth.github.authorize_redirect()

@app_bp.route('/github/callback')
def github_callback():
    token = oauth.github.authorize_access_token()
    return jsonify(token)

@app_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))




"""
    HELPER FUNCTIONS
"""
# scope validating decorator
"""def require_scope(scope):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header()

            try:
                payload = oauth.auth0.token_parse_id(token)
                if scope in payload.get('scope', '').split():
                    return f(*args, **kwargs)
                else:
                    raise OAuthError(
                        'error': 
                    )
            except Exception as e:
                raise OAuthError()
        return decorated
    return decorator


def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise OAuthError()
    parts = auth_header.split()
    if parts[0].lower() != 'bearer':
        raise OAuthError()
    elif len(parts) == 1:
        raise OAuthError()
    elif len(parts) > 2:
        raise OAuthError()
    return parts[1]
"""
