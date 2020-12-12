from flask import request
from flask_restful import Resource
from ..models.user import User
from ..db import db


class Users(Resource):
    def get(self):
        found_users = User.query.all()
        if found_users:
            return [user.to_json() for user in found_users], 200

        return {'message': 'No users found'}, 404


class UserRegister(Resource):

    def post(self):
        data = request.get_json()
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_json(), 201


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        found_user = User.query.filter_by(email=data['email']).first()
        if found_user and found_user.password == data['password']:
            access_token = create_access_token(identity=found_user.id, fresh=True)
            refresh_token = create_refresh_token(found_user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials'}, 401
