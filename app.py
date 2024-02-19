from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from models import User , db




app = Flask(__name__)

# Configure the app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["JWT_SECRET_KEY"] = "wsddf542455r5rdd55d579j8f6f8yfrd57tru
db = SQLAlchemy(app)

@app.route('/signup', methods=['POST'])
def signup():
    data=request.json
    
    username=data.get('username')
    email=data.get('email')
    password=data.get('password')
    
    if not email or not password:
        return jsonify({'message':'email and password are required'},400)
    
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    
    existing_user = (
            User.query.filter_by(username=username).first()
            or User.query.filter_by(email=email).first()
        )
    
    if existing_user:
        return (
            jsonify({
                "message":"username or email already exists.please choose another"
            }
            ),400        
        )
    new_user = User(username=username, email=email)
    new_user.set_password(password)   
    
    
    db.session.add(new_user)
    db.session.commit()
    
    return (
            jsonify({"message": "User registered successfully!"}),
            201,
        )
