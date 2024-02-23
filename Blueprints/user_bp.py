from flask import Blueprint,jsonify
from models import User

user_bp=Blueprint("user",__name__)

@user_bp.route("/users")
def get_users():
    users=User.query.all()
    users_list=[]
    if users:
        for user in users:
            users_dict = {
                "id": user.id,
                "email": user.email,
                "phone_number": user.phone_number,  
                "role": user.role
            }
            users_list.append(users_dict)
            
        return {"Users" : users_list}
    else:
        return jsonify(message="No Users Found"),404
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    user=User.query.filter_by(id=user_id).first()
    if user:
        return jsonify({
            "id": user.id,
            "email": user.email,
            "phone_number": user.phone_number,  
            "role": user.role
        }),200
        
    else:
        return jsonify({"message":"User Not Found"}),404  
    

# =======
# from flask import Blueprint, jsonify, request
# from models import User, db
# user_bp=Blueprint("user",__name__)



# user_bp = Blueprint("user", __name__)

# @user_bp.route('/users', methods=['POST'])
# def create_user():
#     data = request.json
#     new_user = User(
#         name=data['name'],
#         email=data['email'],
#         phone_number=data['phone_number'],
#         password=data['password'],
#         role=data.get('role', 'User')
#     )
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'User created successfully'}), 201

# @user_bp.route('/users', methods=['GET'])
# def get_users():
#     users = User.query.all()
#     result = [{'id': user.id, 'name': user.name} for user in users]
#     return jsonify({'users': result}), 200

# @user_bp.route('/users/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     user = User.query.get(user_id)
#     if user:
#         return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 200
#     else:
#         return jsonify({'message': 'User not found'}), 404

# @user_bp.route('/users/<int:user_id>', methods=['PATCH'])
# def update_user(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({'message': 'User not found'}), 404
#     data = request.json
#     user.name = data.get('username', user.name)
#     user.email = data.get('email', user.email)
#     user.password = data.get('password', user.password)
#     user.role = data.get('role', user.role)
#     db.session.commit()
#     return jsonify({'message': 'User updated successfully'}), 200

# @user_bp.route('/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({'message': 'User not found'}), 404
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({'message': 'User deleted successfully'}), 200
# >>>>>>> dev
