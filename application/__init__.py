import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

from .resources.fooditems import FoodItems
from .resources.messmenu import MessMenu
from .resources.donations import Donate, Receive, History
from .resources.user import (
    UserRegister,
    UserLogin,
    UserDetail,
    UserLogout,
    TokenRefresh
)

from .db import db
from .blacklist import BLACKLIST


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['JWT_SECRET_KEY'] = 'abcd@1234'
    api = Api(app)

    db.init_app(app)
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        return decrypted_token['jti'] in BLACKLIST

    api.add_resource(FoodItems, '/items')
    api.add_resource(MessMenu, '/menu')
    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(UserDetail, '/user')
    api.add_resource(TokenRefresh, '/refresh')
    api.add_resource(Donate, '/donate')
    api.add_resource(Receive, '/receive')
    api.add_resource(History, '/history')

    with app.app_context():
        db.create_all()
        return app
