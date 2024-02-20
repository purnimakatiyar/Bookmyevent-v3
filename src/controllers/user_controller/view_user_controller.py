"""
This module contains the ViewUserController class, which handles requests related to viewing user information in a Flask application.
"""
import logging
from businesslogic.user_business import User
from utils.exceptions import DBException, CustomException
from settings.constants import Constants
from flask import jsonify
logger = logging.getLogger('view_user_controller')


class ViewUserController:
    """
    ViewUserController: Handles user information viewing operations.
    """
    
    def __init__(self):
        self.user = User()

    def users_list_to_dict(self, managers):
        """
        Retrieves a list of all managers in the system and returns them as a JSON response.
        """
        result_list = []
        for manager in managers:
            user_id, username, name, phone = manager
            event_dict = {Constants.USERNAME: username,
                              Constants.NAME: name,
                             Constants.PHONE: phone,
                         }
            result_list.append(event_dict)
            
        return {Constants.STATUS: 200, Constants.MANAGERS: result_list}
        
    
    def list_managers(self):
        """
        Retrieves a list of all managers in the system and returns them as a JSON response.
        """
        try:
            managers = self.user.list_all_managers()
            success_result = self.users_list_to_dict(managers)
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
            
            
    def view_profile(self, user_id):
        """
        Retrieves the profile information of a user with the specified user ID and returns it as a JSON response.
        """
        
        try:
            result = self.user.view_profile(user_id)
            success_result = {Constants.STATUS: 200, 
                    Constants.USERNAME: result[1],
                    Constants.NAME: result[2],
                    Constants.PHONE: result[3],
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