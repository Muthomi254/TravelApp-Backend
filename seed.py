from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Travelling_service, Accomodation_service, Company, Review_travel, Review_accomodation, Reservation_accomodation, Reservation_travel, Travel_booking, Accomodation_booking
from datetime import datetime
import random
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Create application context
app.app_context().push()

# Now you can interact with the database within the application context

from faker import Faker
fake = Faker()


def create_users():
    try:
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
        print("..............................Users created successfully!...........................")
    except Exception as e:
        db.session.rollback()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Error creating users:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", str(e))

def create_companies():
    try:
        for _ in range(5):
            company = Company(
                name=fake.company(),
                email=fake.company_email(),
                password=fake.password(),
                description=fake.text(),
                category=random.choice(['Transport', 'Accommodation'])
            )
            db.session.add(company)
        db.session.commit()
        print("...............................Companies inserted successfully!........................")
    except Exception as e:
        db.session.rollback()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Error inserting companies:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", str(e))


def create_travelling_services():
    try:
        for _ in range(10):
            service = Travelling_service(
                name=fake.word(),
                seats=random.randint(1, 100),
                depurture_time=fake.date_time(),
                arrival_time=fake.date_time(),
                description=fake.text(),
                price=random.uniform(100, 1000),
                depurture_city=fake.city(),
                arrival_city=fake.city(),
                registration_number=fake.unique.random_number(9),
                company_id=random.randint(1, 5)
            )
            db.session.add(service)
        db.session.commit()
        print("..................................Travelling services created successfully!....................................")
    except Exception as e:
        db.session.rollback()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Error creating travelling services:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", str(e))

def create_accomodation_services():
    try:
        for _ in range(10):
            service = Accomodation_service(
                name=fake.word(),
                location=fake.address(),
                available_rooms=random.randint(1, 50),
                images=fake.image_url(),
                price_per_night=random.uniform(50, 500),
                average_rating=random.uniform(1, 5),
                company_id=random.randint(1, 5)
            )
            db.session.add(service)
        db.session.commit()
        print(".........................Accommodation services created successfully!...................")
    except Exception as e:
        db.session.rollback()
        print("!!!!!!!!!!!!!!!!!!!!Error creating accommodation services:!!!!!!!!!!!!!!!!!!!!!!!!!!!!", str(e))

def create_reviews():
    try:
        for _ in range(20):
            review_travel = Review_travel(
                rating=random.uniform(1, 5),
                review=fake.text(),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                user_id=random.randint(1, 10),
                travel_id=random.randint(1, 10),
                review_count=random.randint(1, 100)
            )
            db.session.add(review_travel)

            review_accomodation = Review_accomodation(
                rating=random.uniform(1, 5),
                review=fake.text(),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                user_id=random.randint(1, 10),
                accomodation_id=random.randint(1, 10),
                review_count=random.randint(1, 100)
            )
            db.session.add(review_accomodation)
        db.session.commit()
        print(".................Reviews created successfully!.............................")
    except Exception as e:
        db.session.rollback()
        print("!!!!!!!!!!!!!!!!!!!!!!!!Error creating reviews:!!!!!!!!!!!!!!!!!!!!!!", str(e))

def create_reservations():
    try:
        for _ in range(10):
            # Create a random user
            user = User.query.get(random.randint(1, 10))

            # Create a random Accomodation_service and Travelling_service
            accomodation_service = Accomodation_service.query.get(random.randint(1, 10))
            travelling_service = Travelling_service.query.get(random.randint(1, 10))

            # Create Reservation_accomodation associated with Accomodation_service
            reservation_accomodation = Reservation_accomodation(
                people_included=random.randint(1, 5),
                date=datetime.now(),
                checkin=fake.date_time_this_year(),
                checkout=fake.date_time_this_year(),
                days_in_room=random.randint(1, 10),
                rooms=random.randint(1, 3),
                user=user,  # Set user directly
                service_id=accomodation_service.id,
                price_net=random.randint(100, 1000)
            )
            db.session.add(reservation_accomodation)

            # Create Reservation_travel associated with Travelling_service
            reservation_travel = Reservation_travel(
                people_included=random.randint(1, 5),
                date=datetime.now(),
                user=user,  # Set user directly
                service_id=travelling_service.id
            )
            db.session.add(reservation_travel)

        db.session.commit()
        print(".....................Reservations created successfully.................!")
    except Exception as e:
        db.session.rollback()
        print("!!!!!!!!!!!!!!!!!!!!!!!!Error creating reservations:!!!!!!!!!!!!!!!!!!!!", str(e))

def create_bookings():
    try:
        for _ in range(10):
            # Create instances of related models first
            reservation_accomodation = Reservation_accomodation.query.get(random.randint(1, 10))
            accomodation_service = Accomodation_service.query.get(random.randint(1, 10))

            # Create Accomodation_booking associated with Reservation_accomodation and Accomodation_service
            accomodation_booking = Accomodation_booking(
                accomodation_reservation=reservation_accomodation,
                accomodation_service=accomodation_service,
                user_id=random.randint(1, 10)  # Add this line to set user_id
            )
            db.session.add(accomodation_booking)

            # Repeat the process for Travel_booking
            reservation_travel = Reservation_travel.query.get(random.randint(1, 10))
            travelling_service = Travelling_service.query.get(random.randint(1, 10))

            travel_booking = Travel_booking(
                travelling_reservation=reservation_travel,
                travelling_service=travelling_service,
                user_id=random.randint(1, 10)  # Add this line to set user_id
            )
            db.session.add(travel_booking)

        db.session.commit()
        print("..............Bookings created successfully!............")
    except Exception as e:
        db.session.rollback()
        print("!!!!!!!!!!!!Error creating bookings:!!!!!!!!!!!!", str(e))

if __name__ == "__main__":
    try:
        db.create_all()
        create_users()
        create_companies()
        create_travelling_services()
        create_accomodation_services()
        create_reviews()
        create_reservations()
        create_bookings()
    except Exception as e:
        print("!!!!!!!!!!!!!!!!An error occurred:!!!!!!!!!!!!!!!!!!!", str(e))
