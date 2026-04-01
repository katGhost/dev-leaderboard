from authlib.integrations.flask_client import OAuth
from app.config import Config

oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)

    # Register the OAuth
    oauth.register(
        'auth0',
        client_id=f'{Config.AUTH0_CLIENT_ID}',
        client_secret=f'{Config.AUTH0_CLIENT_SECRET}',
        # server_metadata_url=f'https://{Config.AUTH0_DOMAIN}/.well-known/openid-configuration',
        api_base_url=f'https://{Config.AUTH0_DOMAIN}',
        access_token_url=f'https://{Config.AUTH0_DOMAIN}/oauth/token',
        authorize_url=f'https://{Config.AUTH0_DOMAIN}/authorize',
        client_kwargs={
            'scope': 'openid profile email'
        },
    )

    # github
    oauth.register(
        'github',
        client_id=app.config['GITHUB_CLIENT_ID'],
        client_secret=app.config['GITHUB_CLIENT_SECRET'],
        access_token_url=f'{app.config["GITHUB_API_BASE_URL"]}/login/oauth/access_token',
        authorize_url=f'{app.config["GITHUB_API_BASE_URL"]}login/oauth/authorize',
        api_base_url=f'{app.config["GITHUB_API_BASE_URL"]}',
        client_kwargs={
            'scope': 'read:user repo'
        },
    )