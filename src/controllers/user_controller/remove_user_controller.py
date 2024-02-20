"""
This module contains the RemoveUserController class, which is responsible for handling requests related to removing managers in a Flask application.
"""
import logging
from businesslogic.user_business import User
from utils import logs
from utils.exceptions import DBException, CustomException
from settings.constants import Constants 
from flask import jsonify
logger = logging.getLogger('remove_user_controller')


class RemoveUserController:
    """
    RemoveUserController class Handles manager removal operations.
    """
    def __init__(self):
        self.user = User()
        
        
    def remove_manager(self, username):
        """
        Removes a manager with the specified username from the system.
        """
        try:
            user = self.user.get_user(username)
            result = self.user.remove_manager(username)
            logs.remove_manager(username)
            
            success_result = {
                            Constants.STATUS: 200,
                            Constants.MESSAGE: Constants.REMOVE_MANAGER_MSG
                            }
            return jsonify(success_result),success_result["status"]
                    
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            failure_result = {
                Constants.STATUS: err.status,
                Constants.ERROR: err.error,
                Constants.MESSAGE: err.message
            }
            
            return jsonify(failure_result),failure_result["status"]