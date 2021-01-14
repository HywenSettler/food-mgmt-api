from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


from ..models.donation import Donation
from ..models.menuitem import MenuItem
from ..models.user import User
from ..db import db


class Donate(Resource):
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        for foodId, quantity in data.items():
            new_donation = Donation(donor=user_id, foodId=foodId, quantity=quantity)
            db.session.add(new_donation)
            db.session.commit()

        return {'message': 'Donation was successful'}, 201


class Receive(Resource):
    @jwt_required
    def get(self):
        food_id = request.args.get('foodId')
        found_donations = Donation.query.filter_by(foodId=food_id, recipient=None).all()
        ret_arr = []
        for donation in found_donations:
            found_item = MenuItem.query.filter_by(id=donation.foodId).first()
            found_donor = User.query.filter_by(id=donation.donor).first()
            ret_arr.append({
                'id': donation.id,
                'donor': found_donor.to_json(),
                'food': {
                    **found_item.to_json(),
                    'quantity': donation.quantity
                }
            })

        return ret_arr, 200

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        found_donation = Donation.query.filter_by(id=data['donationId']).first()
        found_donation.recipient = user_id
        db.session.commit()

        return {'message': 'Donation was received successfully'}, 201


class History(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        accept_history = Donation.query.filter_by(recipient=user_id).all()

        ret_arr = []

        for donation in accept_history:
            found_item = MenuItem.query.filter_by(id=donation.foodId).first()
            found_donor = User.query.filter_by(id=donation.donor).first()
            ret_arr.append({
                'id': donation.id,
                'donor': found_donor.to_json(),
                'food': {
                    **found_item.to_json(),
                    'quantity': donation.quantity
                }
            })

        return ret_arr, 200
