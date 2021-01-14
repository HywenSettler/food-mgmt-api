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
        item_type = request.args.get('type')
        search_query = request.args.get('searchQuery')
        # select * from menuitems where type=item_type and name ilike "%{searchQuery}%"
        if not item_type:
            found_items = db.session.query(
                MenuItem.name.distinct()).filter(
                MenuItem.name.ilike(f"%{search_query}%")).all()
        else:
            found_items = MenuItem.query.filter_by(
                type=mapping.get(item_type)).filter(
                MenuItem.name.ilike(f"%{search_query}%")).all()

        return [item.to_json() for item in found_items], 200

    def post(self):
        data = request.get_json()
        for food_item in data:
            new_item = MenuItem(food_item['name'], mapping.get(food_item['type']), food_item['image_url'])
            db.session.add(new_item)
            db.session.commit()
        return {'message': 'Items added to DB successfully'}, 201
