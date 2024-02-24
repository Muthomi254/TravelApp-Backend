from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from faker import Faker
import random
import os

from app import app,db
fake = Faker()

# Import your models
from models import User, Travelling_service, Accomodation_service, Company, Review_travel, Review_accomodation, Reservation_travel, Reservation_accomodation, Travel_booking, Accomodation_booking

# Initialize Flask app and configure Flask app with the database URI
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
# db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Seed data
with app.app_context():
    # Seed Users
    for _ in range(10):
        user = User(
            name=fake.name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            password=generate_password_hash(fake.password()),
            role=random.choice(['Admin', 'User'])
        )
        db.session.add(user)

    db.session.commit()

    # Seed Companies
    for _ in range(5):
        company = Company(
            name=fake.company(),
            email=fake.email(),
            password=generate_password_hash(fake.password()),
            description=fake.text(),
            category=random.choice(['Transport', 'Accommodation'])
        )
        db.session.add(company)

    db.session.commit()

    # Seed Travelling_services
    companies = Company.query.all()
    for _ in range(20):
        travelling_service = Travelling_service(
            name=fake.word(),
            seats=fake.random_int(min=1, max=100),
            depurture_time=fake.date_time(),
            arrival_time=fake.date_time(),
            description=fake.text(),
            price=fake.random_int(min=10, max=1000),
            depurture_city=fake.city(),
            arrival_city=fake.city(),
            registration_number=fake.uuid4(),
            company=random.choice(companies)
        )
        db.session.add(travelling_service)

    db.session.commit()

    # Seed Accomodation_services
    for _ in range(15):
        accomodation_service = Accomodation_service(
            name=fake.word(),
            location=fake.word(),
            available_rooms=fake.random_int(min=1, max=100),
            images=fake.image_url(),
            price_per_night=fake.random_int(min=50, max=500),
            average_rating=fake.pyfloat(min_value=1, max_value=5, right_digits=1),
            company=random.choice(companies)
        )
        db.session.add(accomodation_service)

    db.session.commit()

    # Seed Reviews
    users = User.query.all()
    travels = Travelling_service.query.all()
    accomodations = Accomodation_service.query.all()

    for _ in range(30):
        review_travel = Review_travel(
            rating=fake.pyfloat(min_value=1, max_value=5, right_digits=1),
            review=fake.text(),
            user=random.choice(users),
            travel=random.choice(travels)
        )
        db.session.add(review_travel)

        review_accomodation = Review_accomodation(
            rating=fake.pyfloat(min_value=1, max_value=5, right_digits=1),
            review=fake.text(),
            user=random.choice(users),
            accomodation=random.choice(accomodations)
        )
        db.session.add(review_accomodation)

    db.session.commit()

    # Seed Reservations
    for _ in range(10):
        reservation_travel = Reservation_travel(
            people_included=fake.random_int(min=1, max=5),
            date=fake.date_time(),
            user=random.choice(users)
        )
        db.session.add(reservation_travel)

        reservation_accomodation = Reservation_accomodation(
            people_included=fake.random_int(min=1, max=5),
            date=fake.date_time(),
            checkin=fake.date_time(),
            checkout=fake.date_time(),
            days_in_room=fake.random_int(min=1, max=10),
            rooms=fake.random_int(min=1, max=5),
            user=random.choice(users)
        )
        db.session.add(reservation_accomodation)

    db.session.commit()

    # Seed Bookings
    reservation_travels = Reservation_travel.query.all()
    reservation_accomodations = Reservation_accomodation.query.all()

    new_Travel_booking = Travel_booking(
    travelling_reservation=random.choice(reservation_travels),
    travelling_service=random.choice(travels)
    )
    db.session.add(new_Travel_booking)


    accomodation_booking = Accomodation_booking(
    accomodation_reservation=random.choice(reservation_accomodations),
    accomodation_service=random.choice(accomodations)
    )
    db.session.add(accomodation_booking)

    db.session.commit()
