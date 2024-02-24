from flask import request, jsonify, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required,unset_jwt_cookies,get_jwt_identity
from models import db, User, RevokedToken

auth_bp = Blueprint('auth_bp', __name__)

# add user
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    user = User.query.filter_by(email=email).first()

    if user:
        stored_password = user.password
        if check_password_hash(stored_password, password):
            access_token = create_access_token(identity=user.id)
            return jsonify({"msg":"succesfully loged in" ,"access_token":access_token}), 200
        else:
            return jsonify({"error": "Incorrect Password!"}), 401
    else:
        return jsonify({"error": "User not found!"}), 404
# create user
@auth_bp.route('/register', methods=['POST'])
def create_user():
    data=request.get_json()
    email=data['email']
    password=generate_password_hash(data['password'])
    phone_number=data['phone_number']
    name=data['name']
    role=data['role']
    
    
    try:
        new_user = User(email=email, password=password, name=name, role=role, phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "New user created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400




Logout user
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200


# @auth_bp.route("/logout", methods=["POST"])
# @jwt_required()
# def logout():
#     try:
#         # Get the token's jti (JWT ID) from the decoded token
#         jti = get_jwt_identity()['jti']
        
#         # Add the token's jti to the revoked token list
#         revoked_token = RevokedToken(jti=jti)
#         db.session.add(revoked_token)
#         db.session.commit()

#         # Clear the JWT cookies from the response
#         response = jsonify({"msg": "Logout successful"})
#         unset_jwt_cookies(response)
        
#         return response, 200
#     except Exception as e:
#         # Handle any errors
#         return jsonify({"error": str(e)}), 500

@auth_bp.route("/profile/<int:user_id>", methods=["GET"])
@jwt_required()
def get_current_user(user_id):
    current_user = User.query.filter_by(id=user_id).first()
        
    if current_user:
        if current_user.id == get_jwt_identity():

            if isinstance(current_user, list) and len(current_user) > 0:
                # Use the first element if it's a list
                current_user = current_user[0]

            return jsonify({
                "id": current_user.id,
                "name": current_user.name,
                "phone_number": current_user.phone_number,
            })
        else:
            return jsonify({"message": "You are unauthorized to access this resource."}), 403
    else:
        return jsonify({"error": "User not found"}), 404
   

@auth_bp.route("/delete_user/<int:user_id>", methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user=User.query.filter_by(id=user_id).first()
    
    if user is None or user.id != get_jwt_identity():
        return jsonify({"error":"No such user or unauthorized access."}),4
    else:
        
        db.session.delete(user)
        db.session.commit()
        return{"msg":"user deleted sucssesfully"}
        
# remember to add a change password
@auth_bp.route('/change_password/<int:user_id>',methods=['PUT'])
@jwt_required()
def change_password(user_id):
    user=User.query.filter_by(id=user_id).first()
    if  user is None:
        return  jsonify({"error":"The user does not exist."}) , 404
    else:
        data=request.json
        new_password=data['password']
        user.password=generate_password_hash(new_password)
        db.session.commit()
        return jsonify( {"msg":"Password has been changed successfully."} ),200
    
        
        
# remember to add a update profile
@auth_bp.route('/update_profile/<int:user_id>', methods = ['POST'])
@jwt_required()
def update_profile(user_id):
    user = User.query.filter_by(id = user_id).first()
    if user:
        if user.id == get_jwt_identity():
            data=request.get_json()
            for key,value in data.items():
                if key == "email":
                    user.password=value
                elif key=='name':
                    user.name = value
                elif key == "phone_number":
                    user.phone_number = value
            db.session.commit()
            return jsonify( {'msg':'Profile updated Successfully'} ),200
        else:
            return jsonify({ 'error':'You do not have permission to edit this user.' }),403
    else:
        return jsonify( {'error':'User does not exist'} ) ,404
    