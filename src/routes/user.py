from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint
from schema import UserSchema,UpdateUserSchema
from controllers.user_controller.add_user_controller import AddUserController
from controllers.user_controller.remove_user_controller import RemoveUserController
from controllers.user_controller.update_user_controller import UpdateUserController
from controllers.user_controller.view_user_controller import ViewUserController
from utils.rbac import role_access
from flask_jwt_extended import jwt_required, get_jwt
from flask import request

blp = Blueprint("User", "user", description="User operations")


@blp.route('/signup')
class UserView(MethodView):
    
    @blp.arguments(UserSchema)
    def post(self, user_data):
        auth = AddUserController()
        response = auth.signup(user_data)
        return jsonify(response), response["status"]
        

@blp.route('/manager')
class ManagerView(MethodView):
    
    @jwt_required()
    @role_access(['Admin'])
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', \
                    'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.arguments(UserSchema)
    def post(self, user_data):
        
        user = AddUserController()
        response = user.add_user(user_data)
        return response
    
@blp.route('/managers')
class UsersView(MethodView):
    
    @jwt_required()
    @role_access(['Admin'])
    def get(self):
        user = ViewUserController()
        return user.list_managers()
        

@blp.route('/managers/<user_id>')
class ManagerControlView(MethodView):
    '''Method for remove manager by admin'''
    @jwt_required()
    @role_access(['Admin'])
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', \
                    'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    
    def delete(self, user_id):

        user = RemoveUserController()
        return user.remove_manager(user_id)
        
            

@blp.route('/profile')
class ProfileView(MethodView):
      
    @jwt_required()
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', \
                    'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def get(self):
        payload = get_jwt()
        user = ViewUserController()
        return user.view_profile(payload["id"])
       
       
# @blp.route('/users')
# class UserOperationView(MethodView):
      
    @jwt_required()
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.arguments(UpdateUserSchema)
    def put(self, user_data):
        
        payload = get_jwt()
        user = UpdateUserController()
        response = user.update_user_details(payload["id"], user_data)
        return response
    