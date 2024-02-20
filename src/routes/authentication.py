from flask.views import MethodView
from flask_smorest import Blueprint
from schema import AuthSchema
from controllers.auth_controller.login_controller import LoginController
from controllers.auth_controller.logout_controller import LogoutController
from flask_jwt_extended import jwt_required

blp = Blueprint("Auth", "auth", description="Authenticate operations")


@blp.route('/login')
class AuthenticateView(MethodView):
    
    @blp.arguments(AuthSchema)
    def post(self, auth_data):
        print("0")
        auth = LoginController()
        print("hhhhhhhhhhhhhh")
        response = auth.login(auth_data)
        return response
        
        
@blp.route("/refresh")
class RefreshToken(MethodView):

    @jwt_required(refresh=True)
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 
                'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def post(self):
        auth = LoginController()
        auth.refresh_token()
        
@blp.route('/logout')
class LogoutView(MethodView):
    
    @jwt_required()
    def post(self):
        auth = LogoutController()
        result = auth.logout()
        return result