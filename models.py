from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db=SQLAlchemy()

class User(db.Model, SerializerMixin):
    
    __tablename__ = "Users"
    
    id =db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    phone_number=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(80),nullable=False)
    role=db.Column(db.Enum('Admin', 'User'),default="User", nullable=False, server_default="User")
    
    
class Travelling_service(db.Model, SerializerMixin):
    
    __tablename__ = "travelling_services"
    
    id= db.Column("ts_id",db.Integer, primary_key=True)
    name=db.Column(db.String(64), nullable=False)
    seats=db.Column(db.Integer, default=1)
    depurture_time=db.Column(db.DateTime, nullable=False)
    arrival_time=db.Column(db.DateTime, nullable=False)
    description=db.Column(db.Text)
    price=db.Column(db.Float, nullable=False)
    depurture_city=db.Column(db.String(32), nullable=False)
    arrival_city=db.Column(db.String(32), nullable=False)
    registration_number = db.Column(db.String(9), unique=True)
    
    company_id=db.Column(db.String(6),db.ForeignKey('companies.id'))

class Accomodation_service(db.Model, SerializerMixin):
    
    __tablename__ = "accomodation_services"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    available_rooms = db.Column(db.Integer, default=0) 
    images = db.Column(db.String(255), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    average_rating = db.Column(db.Float, nullable=False)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

class Company(db.Model, SerializerMixin):
    
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    description = db.Column(db.String)
    category = db.Column(db.Enum('Transport', 'Accommodation'))
    
    accomodation_services = db.relationship('Accomodation_service', backref='company')
    traveling_services = db.relationship('Travelling_service', backref='company')
    
class Review_travel(db.Model, SerializerMixin):
    __tablename__ = "Reviews(travels)"
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())    
    
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete="CASCADE"), nullable=False)
    travel_id = db.Column(db.String(6), db.ForeignKey('travelling_services.ts_id'), nullable=False)  # Update this line
    review_count = db.Column(db.Integer, default=0)
    
    travel = db.relationship('Travelling_service', backref='reviews')


    
    
    
class Review_accomodation(db.Model, SerializerMixin):
    __tablename__ = "Reviews(accomodation)"
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())    
    
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete="CASCADE"), nullable=False)  # Update this line
    accomodation_id = db.Column(db.String(9), db.ForeignKey('accomodation_services.id'))
    review_count = db.Column(db.Integer, default=0)
    
    accomodation = db.relationship('Accomodation_service', backref='reviews')


    

class Reservation_travel(db.Model, SerializerMixin):

    __tablename__ ="reservation(travels)"

    
    id = db.Column(db.Integer, primary_key=True)
    people_included = db.Column(db.SmallInteger, nullable=False)
    date = db.Column(db.DateTime(), server_default=db.func.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete="CASCADE"), nullable=False)  # Update this line
    user = db.relationship('User', backref="reservation_accomodation")

    
class Reservation_accomodation(db.Model, SerializerMixin):
    

    __tablename__ ="reservation(accomodation)"

    
    id = db.Column(db.Integer, primary_key=True)
    people_included = db.Column(db.SmallInteger, nullable=False)
    date = db.Column(db.DateTime(), server_default=db.func.now())
    checkin = db.Column(db.Date)
    checkout = db.Column(db.Date)
    days_in_room = db.Column(db.Integer)
    rooms = db.Column(db.Integer)
    
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete="CASCADE"), nullable=False)  # Update this line
    user = db.relationship("User", backref="reservation_travels")
    
    price_net = db.Column(db.Integer)

    
    
class travel_booking(db.Model, SerializerMixin):
    __tablename__ = "travel_bookings"
    
    id = db.Column(db.Integer, primary_key=True)
    travelling_reservation_id = db.Column(db.Integer, db.ForeignKey("reservation(travels).id"))
    travelling_service_id = db.Column(db.Integer, db.ForeignKey("travelling_services.ts_id"))  # Update this line
    
    travelling_reservation = db.relationship("Reservation_travel", backref="travel_bookings")
    travelling_service = db.relationship("Travelling_service", backref="travel_bookings")

    
    
class Accomodation_booking(db.Model, SerializerMixin):
    
    __tablename__ = "accomodation_bookings"
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Fix the relationship definition
    accomodation_reservation_id = db.Column(db.Integer, db.ForeignKey("reservation(accomodation).id"))
    accomodation_service_id = db.Column(db.Integer, db.ForeignKey("accomodation_services.id"))
    
    accomodation_service = db.relationship("Accomodation_service", backref="accomodation_bookings")
    accomodation_reservation = db.relationship("Reservation_accomodation", backref="accomodation_bookings")

class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), unique=True, nullable=False)  # Add unique constraint
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    
    user = db.relationship('User', backref='revoked_tokens')
    company = db.relationship('Company', backref='revoked_tokens')

    @staticmethod
    def is_jti_blacklisted(jwt_header, jwt_data):
        jti = jwt_data['jti']
        query = RevokedToken.query.filter_by(jti=jti).first()
        return bool(query)


