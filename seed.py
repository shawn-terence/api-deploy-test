#!/usr/bin/env python3
# server/seed.py

from app import app
from models import db, Product, Category, User, Profile

with app.app_context():
    Product.query.delete()

    Category.query.delete()
    User.query.delete()
    Profile.query.delete()


    category1 = Category(name='Action')
    category2 = Category(name='Drama')
    category3 = Category(name='Comedy')
    category4 = Category(name='Adventure')

    db.session.add(category1)
    db.session.add(category2)
    db.session.add(category3)
    db.session.add(category4)

    db.session.commit()

    product1 = Product(name='The Matrix', description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', price=10, category=category1)
    product2 = Product(name='The Shawshank Redemption', description='Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', price=15, category=category2)
    product3 = Product(name='The Hangover', description='Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing.', price=8, category=category3)
    product4 = Product(name='Jurassic Park', description='During a preview tour, a theme park suffers a major power breakdown that allows its cloned dinosaur exhibits to run amok.', price=12, category=category4)

    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)
    db.session.add(product4)

    db.session.commit()


    user1 = User(username='Alice', password='password1')
    user2 = User(username='Bob', password='password2')
    user3 = User(username='Charlie', password='password3')


    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)


    db.session.commit()

    profile1 = Profile(fullname='Alice Anderson', user=user1)
    profile2 = Profile(fullname='Bob Brown', user=user2)
    profile3 = Profile(fullname='Charlie Chapman', user=user3)

    db.session.add(profile1)
    db.session.add(profile2)
    db.session.add(profile3)

    db.session.commit()
