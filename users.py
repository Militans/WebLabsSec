from flask_sqlalchemy import SQLAlchemy
import hashlib
import os

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    salt = db.Column(db.String(32), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.salt = os.urandom(16).hex()
        self.password_hash = self._hash_password(password)

    def _hash_password(self, password):
        return hashlib.sha256((password + self.salt).encode('utf-8')).hexdigest()


