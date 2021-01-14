from ..db import db


class Donation(db.Model):
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True)
    donor = db.Column(db.Integer)
    recipient = db.Column(db.Integer)
    foodId = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
