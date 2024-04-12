#!/usr/bin/env python3
# server/seed.py

from app import app
from models import db, Product, Category, User, Profile

with app.app_context():
    # Delete all rows in the "products" table
    Product.query.delete()

    # Delete all rows in the "categories" table
    Category.query.delete()

    # Delete all rows in the "users" table
    User.query.delete()

    # Delete all rows in the "profiles" table
    Profile.query.delete()

    # Create categories
    category1 = Category(name='Phone')
    category2 = Category(name='Shoes')

    # Add categories to the session
    db.session.add(category1)
    db.session.add(category2)

    # Commit changes to the database
    db.session.commit()

    # Create products
    product1 = Product(name='Nokia 10', description='Latest model', price=10, category=category1)
    product2 = Product(name='Sketchers', description='Light running shoe', price=20, category=category2)

    # Add products to the session
    db.session.add(product1)
    db.session.add(product2)

    # Commit changes to the database
    db.session.commit()

    # Create users
    user1 = User(username='Jeff1', password='password1')
    user2 = User(username='Dan2', password='password2')

    # Add users to the session
    db.session.add(user1)
    db.session.add(user2)

    # Commit changes to the database
    db.session.commit()

    # Create profiles
    profile1 = Profile(fullname='Jeff One', user=user1)
    profile2 = Profile(fullname='Dan Two', user=user2)

    # Add profiles to the session
    db.session.add(profile1)
    db.session.add(profile2)

    # Commit changes to the database
    db.session.commit()
