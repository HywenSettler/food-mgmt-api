from ..db import db
from .menu import menus


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    orgName = db.Column(db.String(100))
    isNGO = db.Column(db.Boolean)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    pincode = db.Column(db.String(6))
    address = db.Column(db.String(200))
    phoneNumber = db.Column(db.String(13))
    profileImageUrl = db.Column(db.String(400))
    menu = db.relationship('MenuItem', secondary=menus, backref=db.backref('users', lazy='dynamic'))

    def to_json(self):
        return {
            'email': self.email,
            'password': self.password,
            'orgName': self.orgName,
            'isNGO': self.isNGO,
            'city': self.city,
            'state': self.state,
            'pincode': self.pincode,
            'address': self.address,
            'phoneNumber': self.phoneNumber,
            'profileImageUrl': self.profileImageUrl
        }
