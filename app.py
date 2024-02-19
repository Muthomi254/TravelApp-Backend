from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # Change this to your database URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to your desired secret key
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)  # Enable CORS for all routes

# Define your models here

# from auth import auth_blueprint
# from accommodation import accommodation_blueprint
# from travel import travel_blueprint

# app.register_blueprint(auth_blueprint)
# app.register_blueprint(accommodation_blueprint)
# app.register_blueprint(travel_blueprint)

# Import your blueprints here


if __name__ == '__main__':
    app.run(debug=True)
