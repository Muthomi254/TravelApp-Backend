from flask import request, jsonify, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from models import db, User

auth_bp = Blueprint('auth_bp', __name__)

# # routes
# # add customer
# @auth_bp.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     email = data['email']
#     password = data['password']
    
#     customer = Customer.query.filter_by(email=email).first()

#     if customer:
#         stored_password = customer.password
#         # Use check_password_hash to verify the hashed password
#         if check_password_hash(stored_password, password):
#             access_token = create_access_token(identity=customer.id)
#             return jsonify(access_token=access_token)

#         return jsonify({"error": "Incorrect Password!"}), 401

#     else:
#         return jsonify({"error": "Customer doesn't exist!"}), 404



# # Get logged in customer
# @auth_bp.route("/authenticated_customer", methods=["GET"])
# @jwt_required()
# def authenticated_customer():
#     current_customer_id = get_jwt_identity() 
#     customer = Customer.query.get(current_customer_id)

#     if customer:
#         customer_data = {
#             'id': customer.id,
#             'firstname': customer.firstname,
#             'lastname': customer.lastname,
#             'email': customer.email,
#             'address': customer.address,
#             'phone': customer.phone
#         }
#         return jsonify(customer_data), 200
#     else:
#         return jsonify({"error": "Oops customer not found!"}), 404


# # Logout customer
# @auth_bp.route("/logout", methods=["POST"])
# @jwt_required()
# def logout():
#     jwt_data = get_jwt()
#     jti = jwt_data['jti']

#     token_b = TokenBlocklist(jti=jti)
#     db.session.add(token_b)
#     db.session.commit()

#     return jsonify({"success": "Logged out successfully!"}), 200

# @auth_bp.route("/customers/<int:user_id>/password", methods=["PATCH"])
# @jwt_required()
# def change_password(user_id):
#     current_user_id = get_jwt_identity()

#     # Check if the authenticated user is the same as the one attempting to change the password
#     if current_user_id != user_id:
#         return jsonify({"error": "Unauthorized"}), 401

#     data = request.get_json()
#     new_password = data.get('newPassword')
#     email = data.get('email')

#     # Validate the new password and email (you may add your own validation logic)

#     # Update the password in the database
#     customer = Customer.query.get(user_id)
#     if customer:
#         # Update the password using Flask-Bcrypt's generate_password_hash
#         customer.password = generate_password_hash(new_password).decode('utf-8')
#         db.session.commit()

#         return jsonify({"success": "Password changed successfully!"}), 200
#     else:
#         return jsonify({"error": "Customer not found"}), 404