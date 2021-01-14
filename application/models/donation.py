from ..db import db


class Donation(db.Model):
    __tablename__ = 'donations'

    donor = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.Integer, primary_key=True)
    foodId = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
