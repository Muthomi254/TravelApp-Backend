from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite database for simplicity
app.config['SECRET_KEY'] = 'secret_key'  # Secret key for session management
db = SQLAlchemy(app)

@app.route('/signup', methods=['POST'])
def signup():
    data=request.json
    email=data.get('email')
    password=data.get('password')
    
    if not email or not password:
        return jsonify({'message':'email and password are required'},400)

