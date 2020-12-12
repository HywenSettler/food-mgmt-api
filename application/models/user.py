from ..db import db
from .menu import menus


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))
    menu = db.relationship('MenuItem', secondary=menus, backref=db.backref('users', lazy='dynamic'))

    def to_json(self):
        return {'id': self.id, 'name': self.email, 'password': self.password}
