from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db, User, Travelling_service, Accomodation_service, Company, Review_travel, Review_accomodation, Reservation_accomodation, Reservation_travel, travel_booking, Accomodation_booking

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to your desired secret key

# Initialize SQLAlchemy and Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Initialize JWT and CORS
jwt = JWTManager(app)
CORS(app)  # Enable CORS for all routes


# Import and register your blueprints
from Blueprints.admin_bp import admin_bp
from Blueprints.auth_bp import auth_bp
from Blueprints.booking_bp import booking_bp
from Blueprints.company_bp import company_bp
from Blueprints.review_bp import review_bp
from Blueprints.user_bp import user_bp
from Blueprints.reservation_bp import reservation_bp
from Blueprints.traveling_service_bp import traveling_service_bp
from Blueprints.accomodation_service_bp import accomodation_service_bp



app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(company_bp)
app.register_blueprint(review_bp)
app.register_blueprint(user_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(traveling_service_bp)
app.register_blueprint(accomodation_service_bp)



if __name__ == '__main__':
    app.run(debug=True)




