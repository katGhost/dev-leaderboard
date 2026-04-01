import os
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask
from app.oauth import init_oauth
from app.config import Config



def create_app():
    app = Flask(__name__)

    # Config FIRST
    app.config.from_object('app.config.Config')
    app.secret_key = Config.SECRET_KEY
    if not app.debug:
        app.config['PREFERRED_URL_SCHEME'] = 'https'    # still in dev

    # Initialize OAuth
    init_oauth(app)

    # Register blueprints
    from .routes import app_bp
    app.register_blueprint(app_bp)

    # ProxyFix LAST, after everything is configured
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    return app


