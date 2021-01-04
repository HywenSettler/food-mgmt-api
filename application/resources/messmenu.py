from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models.user import User
from ..models.menuitem import MenuItem
from ..db import db


class MessMenu(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        found_user = User.query.filter_by(id=user_id).first()  # select * from users where id=user_id
        if found_user.menu:
            return [item.to_json() for item in found_user.menu], 200

        return {'message': 'Menu not found'}, 404

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        found_user = User.query.filter_by(id=user_id).first()
        for item_id in data:
            found_item = MenuItem.query.filter_by(id=item_id).first()  # select * from menuitems where id=item_id
            found_user.menu.append(found_item)
        db.session.commit()
        return {'message': 'menu created successfully'}, 201
