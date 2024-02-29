
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies
from models import db, Company, RevokedToken
from werkzeug.security import check_password_hash, generate_password_hash
import random
import string  
from flask import current_app

company_auth_bp = Blueprint('company_auth_bp', __name__)

@company_auth_bp.route('/register', methods=['POST'])
def register_company():
    try:
        data = request.json
        # Check if a company with the provided email already exists
        existing_email = Company.query.filter_by(email=data['email']).first()
        if existing_email:
            return jsonify({'error': 'Company with this email already exists'}), 400
        
        # Check if a company with the provided name already exists
        existing_name = Company.query.filter_by(name=data['name']).first()
        if existing_name:
            return jsonify({'error': 'Company with this name already exists'}), 400
        
        # If the company does not exist, proceed with registration
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@company_auth_bp.route('/login', methods=['POST'])
def login_company():
    try:
        data = request.json
        company = Company.query.filter_by(email=data['email']).first()
        if company:
            if check_password_hash(company.password, data['password']):
                access_token = create_access_token(identity=company.id)
                return jsonify({'access_token': access_token}), 200
            else:
                current_app.logger.error('Password mismatch for company with email: %s', data['email'])
                return jsonify({'error': 'Invalid credentials'}), 401
        else:
            current_app.logger.error('No company found with email: %s', data['email'])
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        current_app.logger.error('Login error: %s', str(e))
        return jsonify({'error': 'An error occurred while processing your request'}), 500



@company_auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_company_profile():
    try:
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@company_auth_bp.route('/profile/<int:company_id>', methods=['GET'])
def get_company_by_id(company_id):
    try:
        company = Company.query.get_or_404(company_id)
        company_data = {
            'id': company.id,
            'name': company.name,
            'email': company.email,
            'description': company.description,
            'category': company.category
        }
        return jsonify(company_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500        

@company_auth_bp.route('/profile', methods=['PATCH'])
@jwt_required()
def update_company_profile():
    try:
        current_user_id = get_jwt_identity()
        company = Company.query.get_or_404(current_user_id)
        data = request.json
        # Update only the specified fields
        if 'name' in data:
            # Check if the new name conflicts with existing names
            existing_company_name = Company.query.filter(Company.name == data['name'], Company.id != current_user_id).first()
            if existing_company_name:
                return jsonify({'error': 'Company name already exists'}), 409  # HTTP status code 409 Conflict
            company.name = data['name']
        if 'email' in data:
            # Check if the new email conflicts with existing emails
            existing_company_email = Company.query.filter(Company.email == data['email'], Company.id != current_user_id).first()
            if existing_company_email:
                return jsonify({'error': 'Company email already exists'}), 409  # HTTP status code 409 Conflict
            company.email = data['email']
        if 'description' in data:
            company.description = data['description']
        if 'category' in data:
            # Check if the provided category is valid
            if data['category'] in ['Transport', 'Accommodation']:
                company.category = data['category']
            else:
                return jsonify({'error': 'Invalid category'}), 400
        db.session.commit()
        return jsonify({'message': 'Company profile updated successfully'}), 200
    except IntegrityError as e:
        error_message = str(e.orig)
        if 'UNIQUE constraint failed: companies.email' in error_message:
            return jsonify({'error': 'Email already exists'}), 409
        elif 'UNIQUE constraint failed: companies.name' in error_message:
            return jsonify({'error': 'Name already exists'}), 409
        else:
            return jsonify({'error': error_message}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@company_auth_bp.route('/profile', methods=['DELETE'])
@jwt_required()
def delete_company_profile():
    try:
        current_user_id = get_jwt_identity()
        company = Company.query.get_or_404(current_user_id)
        db.session.delete(company)
        db.session.commit()
        return jsonify({'message': 'Company profile deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@company_auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        # Get the token's jti (JWT ID) from the decoded token
        jti = get_jwt_identity()

        # Check if the token with the same jti already exists
        existing_token = RevokedToken.query.filter_by(jti=jti).first()
        if existing_token:
            # Token already exists, return error message
            return jsonify({"error": "User is already logged out"}), 400

        # Add the token's jti to the revoked token list
        revoked_token = RevokedToken(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()

        # Clear the JWT cookies from the response
        response = jsonify({"msg": "Logout successful"})
        unset_jwt_cookies(response)

        return response, 200
    except Exception as e:
        # Handle any errors
        return jsonify({"error": str(e)}), 500


@company_auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.json
        email = data.get('email')
        name = data.get('name')
        new_password = data.get('new_password')

        # Check if email, name, and new password are provided
        if not email or not name or not new_password:
            return jsonify({'error': 'Email, name, and new password are required'}), 400

        # Check if a company with the provided email and name exists
        company = Company.query.filter_by(email=email, name=name).first()
        if company:
            # If a matching company is found, update the password with the new one
            company.password = generate_password_hash(new_password)
            db.session.commit()

            # Return a success message
            return jsonify({'message': 'Password updated successfully'}), 200
        else:
            # If no matching company is found, return an error
            return jsonify({'error': 'No matching company found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
