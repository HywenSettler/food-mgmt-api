from ..db import db

'''
menus is intermediary association table because relationship between user and menu-items is many to many.
'''

menus = db.Table('menus',
                 db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                 db.Column('menuitem_id', db.Integer, db.ForeignKey('menuitems.id'))
                 )
