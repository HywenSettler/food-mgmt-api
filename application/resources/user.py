from flask import request
from flask_restful import Resource
import bcrypt
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    get_raw_jwt,
    jwt_refresh_token_required
)


from ..blacklist import BLACKLIST
from ..db import db
from ..models.user import User


def verify_pw(user, given_password):
    hashed_pw = user.password
    return bcrypt.hashpw(given_password.encode('utf8'), hashed_pw) == hashed_pw


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
        # hashing the password
        data['password'] = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt())
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

        if found_user and verify_pw(found_user, data['password']):
            access_token = create_access_token(identity=found_user.id, fresh=True)
            refresh_token = create_refresh_token(found_user.id)

            return {
                **found_user.to_json(),
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }, 200

        return {'message': 'Invalid credentials'}, 422


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)

        return {'access_token': new_token}, 200
