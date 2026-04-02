from datetime import datetime
from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    auth0_id = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(128), nullable=True)
    picture = db.Column(db.String(512), nullable=True)
    nickname = db.Column(db.String(128), nullable=True)
    github_token = db.Column(db.String(256), nullable=True)
    github_username = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'auth0_id': self.auth0_id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
            'nickname': self.nickname,
            'github_username': self.github_username,
        }