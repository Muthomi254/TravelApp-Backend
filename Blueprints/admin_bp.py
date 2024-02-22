from flask import Blueprint,request,jsonify
from models import User,db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,unset_jwt_cookies

admin_bp=Blueprint("admin",__name__)

@admin_bp.route('/admin_login')
def  admin_login():
    data= request.get_json()
    
    email=data['email']
    password=data['password']
    
    admin=User.query.filter_by(email=email).first()
    
    if admin:
        if admin.role =='Admin':
            if check_password_hash(admin.password,password):
                accses_token=create_access_token(identity={"id":admin.id,"role":"Admin"})
                
                return jsonify( {"message":"Logged in Successfully",
                        "access-token":accses_token}),200
            else:
                return{"msg":"Invalid Password"},401
        else:
            return jsonify({"error":"You are not an Admin"}),401
    else:
        return jsonify( {"message":"admin user does not exist"}),404
        
# @admin_bp.route("/admin_delete/<int:user_id>", methods=["DELETE"])
# @jwt_required()
# def admin_delete_user(user_id):
#     admin = User.query.filter_by(id=get_jwt_identity()['id']).first()

#     if admin:
#         # Check if the current user is an admin
#         if admin.role == "Admin":
#             # Check if the user to be deleted exists
#             user_to_delete = User.query.filter_by(id=user_id).first()

#             if user_to_delete:
#                 # Check if the user to be deleted has the role "User"
#                 if user_to_delete.role == "User":
#                     db.session.delete(user_to_delete)
#                     db.session.commit()
#                     return jsonify({"message": "User successfully deleted"}), 200
#                 else:
#                     return jsonify({"error": "You don't have permission to delete users with this role"}), 403
#             else:
#                 return jsonify({"error": "User not found"}), 404
#         else:
#             return jsonify({"error": "Unauthorized access! You are not an admin."}), 401
#     else:
#         return jsonify({"error": "Unauthorized access! Please login first."}), 401

        
@admin_bp.route("/admin_logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200

@admin_bp.route('/admin_suspend/<int:user_id>', methods=['PUT'])
@jwt_required
def admin_suspend_account(user_id):
    current_user = get_jwt_identity()
    admin=User.query._filter_by(id=current_user['id']).first()
    if  admin :
        if "Role" in current_user and current_user["Role"]=="Admin":
            # Checking If The Current user is Admin or not
            user=User.query.filter_by(id=user_id).first()
            if user:
                user.suspended=True
                db.session.commit()

# remove suspension

@admin_bp.route('/admin_remove_suspention/<int:user_id>', methods=['PUT'])
@jwt_required
def admin_remove_suspend_account(user_id):
    current_user = get_jwt_identity()
    admin=User.query._filter_by(id=current_user['id']).first()
    if  admin :
        if "Role" in current_user and current_user["Role"]=="Admin":
            # Checking If The Current user is Admin or not
            user=User.query.filter_by(id=user_id).first()
            if user:
                user.suspended=False
                db.session.commit()
