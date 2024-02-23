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
    

