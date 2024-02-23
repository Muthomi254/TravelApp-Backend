from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import db, Company
from werkzeug.security import check_password_hash, generate_password_hash

company_auth_bp = Blueprint('company_auth_bp', __name__)

@company_auth_bp.route('/register', methods=['POST'])
def register_company():
    data = request.json
    new_company = Company(
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        description=data['description'],
        category=data['category']
    )
    db.session.add(new_company)
    db.session.commit()
    return jsonify({'message': 'Company registered successfully'}), 201

@company_auth_bp.route('/login', methods=['POST'])
def login_company():
    data = request.json
    company = Company.query.filter_by(email=data['email']).first()
    if company and check_password_hash(company.password, data['password']):
        access_token = create_access_token(identity=company.id)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@company_auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_company_profile():
    current_user_id = get_jwt_identity()
    company = Company.query.get_or_404(current_user_id)
    company_data = {
        'id': company.id,
        'name': company.name,
        'email': company.email,
        'description': company.description,
        'category': company.category
    }
    return jsonify(company_data), 200

@company_auth_bp.route('/profile', methods=['PATCH'])
@jwt_required()
def update_company_profile():
    current_user_id = get_jwt_identity()
    company = Company.query.get_or_404(current_user_id)
    data = request.json
    # Update only the specified fields
    if 'name' in data:
        company.name = data['name']
    if 'email' in data:
        company.email = data['email']
    if 'description' in data:
        company.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Company profile updated successfully'}), 200

@company_auth_bp.route('/profile', methods=['DELETE'])
@jwt_required()
def delete_company_profile():
    current_user_id = get_jwt_identity()
    company = Company.query.get_or_404(current_user_id)
    db.session.delete(company)
    db.session.commit()
    return jsonify({'message': 'Company profile deleted successfully'}), 200
