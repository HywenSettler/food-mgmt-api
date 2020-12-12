from flask import request
from flask_restful import Resource
from ..models.menuitem import MenuItem, MenuItemTypeEnum
from ..db import db

mapping = {
    'breakfast': MenuItemTypeEnum.BREAKFAST,
    'lunch': MenuItemTypeEnum.LUNCH,
    'dinner': MenuItemTypeEnum.DINNER
}


class FoodItems(Resource):
    def get(self):
        found_items = MenuItem.query.all()  # select * from menuitems
        if found_items:
            return [item.to_json() for item in found_items], 200

        return {'message': 'Item not found'}, 404

    def post(self):
        data = request.get_json()
        new_item = MenuItem(data['name'], mapping.get(data['type']), data['image_url'])
        db.session.add(new_item)
        db.session.commit()
        return new_item.to_json(), 201
