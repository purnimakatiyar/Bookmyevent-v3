"""
This module provides functionality for handling logout-related requests in the application.
"""
import logging
from businesslogic.logout import Token
from utils.exceptions import DBException, CustomException
from settings.constants import Constants 
from flask_jwt_extended import get_jwt
from flask import jsonify
logger = logging.getLogger('logout_controller')

class LogoutController:
    """
    LogoutController class provides methods for handling logout-related requests.
    """
    def logout(self):
        """
        Handle user logout.
        """
        try:
            result = Token.revoke_token(get_jwt())
            if result is True:
                success_result = {
                    Constants.STATUS: 204
                }
                return jsonify(success_result),success_result["status"]
              
        except (DBException, CustomException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
                
            failure_result = {
               Constants.STATUS: err.status,
               Constants.ERROR: err.error,
               Constants.MESSAGE: err.message 
            }
         
            return jsonify(failure_result),failure_result["status"]
            