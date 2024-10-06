from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Relationship mapping customer to related review
    reviews = db.relationship('Review', back_populates='customer')

    # Association proxy to access items through reviews
    items = association_proxy('reviews', 'item', creator=lambda item_obj: Review(item=item_obj))

    serialize_rules = ('-reviews.customer',)

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Relationship mapping item to related review
    reviews = db.relationship('Review', back_populates='item')

    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)

    # Foreign key to store customer id
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    # Foreign key to store item id
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # Relationship mapping review to related customer
    customer = db.relationship('Customer', back_populates='reviews')

    # Relationship mapping review to related item
    item = db.relationship('Item', back_populates='reviews')

    serialize_rules = ('-customer.reviews', '-item.reviews',)