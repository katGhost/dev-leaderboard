from authlib.integrations.flask_client import OAuth
from app.config import Config

oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)

    oauth.register(
        name='auth0',
        client_id=Config.AUTH0_CLIENT_ID,
        client_secret=Config.AUTH0_CLIENT_SECRET,
        server_metadata_url=f'https://{Config.AUTH0_DOMAIN}/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid profile email'
        },
    )

    oauth.register(
        name='github',
        client_id=app.config['GITHUB_CLIENT_ID'],
        client_secret=app.config['GITHUB_CLIENT_SECRET'],
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize',
        api_base_url='https://api.github.com/',
        client_kwargs={
            'scope': 'read:user repo',
            # tells GitHub to send JSON back instead of form-encoded -> FIX REDIRECTION
            'token_endpoint_auth_method': 'client_secret_post',
        },
    )