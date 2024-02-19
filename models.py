from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db=SQLAlchemy()

class User(db.Model,SerializerMixin):
    
    __tablename__ = "Users"
    
    id =db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.string(100),nullable=False)
    phone_number=db.Column(db.string(50),nullable=False)
    password=db.Column(db.string(80),nullable=False)
    role=db.column(db.String(20))
    
    
class Travelling_service(db.Model,SerializerMixin):
    
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

    
    
class Accomodation_service(db.Model,SerializerMixin):
    
    __tablename__ = "accomodation_services"
    
    id = db.Column(db.String(6), primary_key=True)
    name=db.Column(db.String(64), nullable=False)
    location=db.Column(db.String(128), nullable=False)
    available_rooms=db.Column(db.Integer,default=0) 
    images = db.Column(db.String(255))
    price_per_night=db.Column(db.Float)
    avarage_rating=db.Column(db.Float)
    
    company_id=db.Column(db.String(6),db.ForeignKey('companies.id'))
    
class Company(db.Model,SerializerMixin):
    
    __tablename__='companies'
    
    
    id=db.Column(db.String(6), primary_key=True)
    name=db.Column(db.String(64),index=True,unique=True)
    email=db.Column(db.String(120),unique=True)
    password=db.Column(db.String(128))
    description=db.Column(db.String)
    category = db.Column(db.Enum('Tourist', 'Provider'))
    
    accomodation_services = db.relationship('accomodation_services', backref='company')
    traveling_service= db.relationship('travelling_services',backref="company")
    
    
class Review_travel(db.Model, SerializerMixin):
    __tablename__ = "Reviews(travels)"
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())    
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    travel_id = db.Column(db.String(6), db.ForeignKey('travelling_services.id'), nullable=False)
    review_count = db.Column(db.Integer, default=0)
    
    travel = db.relationship('Travelling_services', backref='reviews')

    
    
    
class Review_accomodation(db.Model,SerializerMixin):
    __tablename__= "Reviews(accomodation)"
    
    id=db.Column(db.Integer,primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    review=db.Column(db.Text())
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())    
    
    user_id=db.Column(db.Integer,db.ForeignKey('users.id', ondelete="CASCADE"),nullable=False)
    accomodation_id=db.Column(db.String(9),db.ForeignKey('accomodation_services.id'))
    review_count=db.Column(db.Integer, default=0)
    
    accomodation = db.relationship('accomodation_services', backref='reviews')

    
class Reservation_accomodation(db.Model,SerializerMixin):
    
    __tablename__ ="reservation(accomodation)"
    
    id=db.Column(db.Integer, primary_key=True)
    people_included=db.Column(db.SmallInteger, nullable=False)
    date = db.Column(db.DateTime(), server_default=db.func.now())
    
    user_id=db.Column(db.Integer,db.ForeignKey('users.id', ondelete="CASCADE"),nullable=False)
    user=db.relationship('users',backref="reservation(accomodation)") 
    
class Reservation_travel(db.Model,SerializerMixin):
    
    __tablename__ ="reservation(travels)"
    
    id=db.Column(db.Integer, primary_key=True)
    people_included=db.Column(db.SmallInteger, nullable=False)
    date = db.Column(db.DateTime(), server_default=db.func.now())
    checkin=db.Column(db.Date)
    checkout=db.Column(db.Date)
    days_in_room=db.Column(db.Integer)
    rooms=db.Column(db.Integer)
    
    
    user_id=db.Column(db.Integer,db.ForeignKey('users.id', ondelete="CASCADE"),nullable=False)
    user=db.relationship("users",backref="reservation(travels)")
    
    price_net=db.Column(db.Integer)
    
    
class travel_booking(db.Model,SerializerMixin):
    __tablename__ = "travel_bookings"
    
    id =db.Column(db.Integer,primary_key=True)
    travelling_reservation_id = db.Column(db.Integer, db.ForeignKey("reservation(travels).id"))
    travelling_service_id = db.Column(db.String(12), db.ForeignKey("travelling_services.id"))
    
    travelling_reservation=db.relationship("travelling_reservation_id",backref="travel_bookings")
    travelling_service=db.relationship("travelling_service_id", backref="travel_bookings")
    
    
class Accomodation_booking(db.Model,SerializerMixin):
    
    __tablename__ = "accomodation_bookings"
    
    id=db.Column(db.Integer,primary_key=True)
    
    accomodation_reservation=db.Column(db.Integer,db.ForeignKey("reservation(accomodation).id"))
    accomodation_service_id =db.Column(db.Integer,db.ForeignKey("accomodation_services.id"))
    
    accomodation_service=db.relationship("accomodation_services" ,backref="accomodation_bookings")
    accomodation_reservation=db.relationship("accomodation_Reservation",backref="accomodation_bookings")
     