
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Change this to your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to your desired secret key
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)  # Enable CORS for all routes

# Define your models here

from Blueprints.admin_bp  import admin_bp
from Blueprints.auth_bp   import auth_bp
from Blueprints.booking_bp  import booking_bp
from Blueprints.company_bp import company_bp
from Blueprints.review_bp import review_bp
from Blueprints.user_bp import user_bp
from Blueprints.reservation_bp import reservation_bp


app.register_blueprint(admin_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(user_bp)
app.register_blueprint(company_bp)
app.register_blueprint(review_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(auth_bp)






# Import your blueprints here


if __name__ == '__main__':
    app.run(debug=True)
