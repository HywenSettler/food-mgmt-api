from ..db import db
import enum


class MenuItemTypeEnum(enum.Enum):
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'


class MenuItem(db.Model):
    __tablename__ = 'menuitems'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    type = db.Column(db.Enum(MenuItemTypeEnum))
    image_url = db.Column(db.String(100))

    def __init__(self, name, type, image_url):
        self.name = name
        self.type = type
        self.image_url = image_url

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.value,
            'image_url': self.image_url
        }
