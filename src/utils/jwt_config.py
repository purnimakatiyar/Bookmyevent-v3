from flask_jwt_extended import JWTManager
from businesslogic.logout import Token
from businesslogic.auth_business import Authenticate
from businesslogic.user_business import User
from flask import jsonify

def initialise_jwt_config(app):
    """Initialising all jwt inbuilt decorators"""

    jwt = JWTManager(app)
    @jwt.additional_claims_loader
    def add_role_to_claims(identity):
        role = Authenticate(username = identity).get_role()
        user_id = User(username = identity).get_user_id(identity)
        return {"role": role,
                "id": user_id}
        
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        Token.revoke_token(jwt_payload)
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return Token.check_token_revoked(jwt_payload)

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )