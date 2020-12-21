import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

from .resources.fooditems import FoodItems
from .resources.messmenu import MessMenu
from .resources.user import UserRegister, UserLogin, UserDetail

from .db import db

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['JWT_SECRET_KEY'] = 'abcd@1234'
    api = Api(app)

    db.init_app(app)
    jwt = JWTManager(app)

    api.add_resource(FoodItems, '/items')
    api.add_resource(MessMenu, '/menu/<string:user_id>')
    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserDetail, '/user')

    with app.app_context():
        db.create_all()
        return app