import os
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask
from app.oauth import init_oauth
from app.extensions import db



def create_app():
    app = Flask(__name__)

    # Config FIRST
    app.config.from_object('app.config.Config')

    print(f'SECRET KEY: ', app.config['SECRET_KEY'])

    app.secret_key = app.config['SECRET_KEY']
    
    app.config['PREFERRED_URL_SCHEME'] = 'https'    # still in dev
    app.config.update(
        SESSION_COOKIE_SECURE=False,  # Set to True in production with HTTPS
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )

    # Initialize extensions
    db.init_app(app)
    
    init_oauth(app)
    

    # Register blueprints
    from .routes import app_bp
    app.register_blueprint(app_bp)

    # create tables if they do not exist
    with app.app_context():
        db.create_all()

    # ProxyFix LAST, after everything is configured
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    return app


