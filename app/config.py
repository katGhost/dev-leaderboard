import os
from dotenv import load_dotenv


load_dotenv()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class Config:
    # App
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Auth0
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI")

    # GitHub
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    GITHUB_API_BASE_URL = "https://api.github.com"
    GITHUB_AUTHORIZATION_URL = os.getenv('GITHUB_AUTHORIZATION_URL')

    # SQLite stored in project root
    SQLALCHEMY_DATABASE_URI = "sqlite:///devleaderboard.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False