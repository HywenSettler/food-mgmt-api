from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    get_raw_jwt
)


from ..blacklist import BLACKLIST
from ..db import db
from ..models.user import User


class UserDetail(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        found_user = User.query.filter_by(id=user_id).first()

        return found_user.to_json(), 200


class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_json(), 201


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out'}, 200


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        found_user = User.query.filter_by(email=data['email']).first()
        if found_user and found_user.password == data['password']:
            access_token = create_access_token(identity=found_user.id, fresh=True)
            refresh_token = create_refresh_token(found_user.id)

            return {
                **found_user.to_json(),
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }, 200

        return {'message': 'Invalid credentials'}, 401
