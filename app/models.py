from time import time
import jwt
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(120), index=True, unique=False)
    last_name = db.Column(db.String(120), index=True, unique=False)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Recipe', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Recipe {}>'.format(self.body)


class Purchases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(140))
    ingredient_type = db.Column(db.String(140))
    quantity = db.Column(db.Float())
    units = db.Column(db.String(140))
    expiration_date = db.Column(db.DateTime)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    binned = db.Column(db.Boolean, default = False)
    binned_timestamp = db.Column(db.DateTime, index=True, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Purchases {}>'.format(self.ingredient)


class ExerciseLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    set_id = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))