import os
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask
from authlib.integrations.flask_client import OAuth

# 
oauth = OAuth()

def create_app():
    app = Flask(__name__)

    # Config FIRST
    app.config.from_object('app.config.Config')
    app.config['PREFERRED_URL_SCHEME'] = 'https'

    # Extensions
    oauth.init_app(app)

    # Register the OAuth
    

    # Register blueprints
    from .routes import app_bp
    app.register_blueprint(app_bp)

    # ProxyFix LAST, after everything is configured
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    return app