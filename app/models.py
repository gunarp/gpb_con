from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ups = db.relationship('UPS', backref='user', lazy=True)
    fedex = db.relationship('Fedex', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UPS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    ship_num = db.Column(db.String(6))
    api_key = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<UPS {}>'.format(self.ship_num)


class Fedex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(64))
    password = db.Column(db.String(64))
    ship_num = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Fedex {}>'.format(self.ship_num)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))