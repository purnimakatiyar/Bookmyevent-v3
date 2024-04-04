"""
This module provides functionality for handling login-related requests in the application.
"""
import logging
from businesslogic.auth_business import Authenticate
from businesslogic.user_business import User
from utils.exceptions import CustomException, DBException
from settings.constants import Constants
from flask import jsonify
logger = logging.getLogger('login_controller')


class LoginController:
    """
    LoginController class provides methods for handling login-related requests.
    """
    
    def login(self, auth_data):
        """
        Handle user login.
        """
        try:
            print("2")
            auth = Authenticate(username = auth_data["username"], password = auth_data["password"])
            response = auth.login()
            if response is not None:
                success_result = {Constants.STATUS: 200, Constants.MESSAGE: "Logged in successfully", Constants.ACCESS_TOKEN: response["access_token"], Constants.REFRESH_TOKEN: response["refresh_token"], "role": response["role"]}
                return jsonify(success_result),success_result["status"]
            
        except (DBException, CustomException) as err:
            
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            failure_result = {Constants.STATUS: err.status,
                    Constants.ERROR: err.error,
                    Constants.MESSAGE : err.message}
            return jsonify(failure_result),failure_result["status"]

    
    def refresh_token(self):
        """
        Refresh access tokens.
        """
        auth = Authenticate()
        auth.refresh_token()
    
