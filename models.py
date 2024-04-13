from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash,check_password_hash

db=SQLAlchemy()

#Join table for many to many relationship
favorite_products = db.Table('favorite_products',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)
class Product(db.Model,SerializerMixin):
    __tablename__="products"
    serialize_rules =('-category','-users',)
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True)
    description=db.Column(db.String(200))
    price=db.Column(db.Integer)
    # foreign Column
    category_id=db.Column(db.Integer,db.ForeignKey("categories.id"))
    #relationship:
    #one-to-many
    category=db.relationship("Category",back_populates='products')
    #many-to-many:
    users=db.relationship("User",secondary=favorite_products,back_populates='products')
class Category(db.Model,SerializerMixin):
    #category is a Parent class to product class
    __tablename__="categories"
    serialize_rules=('-products',)

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True)
    #relationship
    products=db.relationship("Product",back_populates='category',cascade='all, delete-orphan')
class User(db.Model,SerializerMixin):
    __tablename__="users"

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True)
    password=db.Column(db.String(10))

    serialize_rules = ('-profile','-products',)
    #relationships:
    #one-to-one
    profile=db.relationship('Profile',back_populates='user')
    #many-many
    products=db.relationship('Product',secondary=favorite_products,back_populates='users')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

class Profile(db.Model,SerializerMixin):
    __tablename__='profiles'
    id=db.Column(db.Integer,primary_key=True)
    fullname=db.Column(db.String(20))
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))

    serialize_rules = ('-user',)
    #relationship
    user=db.relationship('User',back_populates='profile',)





