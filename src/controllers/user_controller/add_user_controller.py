"""
This module contains the AddUserController class, which is responsible for handling requests related to adding users (both customers and managers) in a Flask application.
"""
import logging
from businesslogic.user_business import User
from utils.exceptions import  CustomException, DBException
from flask import jsonify
from settings.constants import Constants
logger = logging.getLogger('add_user_controller')


class AddUserController:
    """
    AddUserController class Handles user addition operations, including customer and manager registration.
    """
    def __init__(self):
        self.user = User()
        
        
    def signup(self, user_data):
        """
        Registers a new customer user based on the provided user data.
        """
        try: 
            user = User(
            username = user_data["username"],
            password = user_data["password"],
            name = user_data["name"],
            phone = user_data["phone"],
            role = Constants.CUSTOMER
            )
            result = user.signup()
            if result is True:
                success_result = {
                        Constants.STATUS: 200,
                        Constants.MESSAGE: Constants.USER_ADDED_MSG
                    }
                return jsonify(success_result),success_result["status"]
        
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            failure_result = {Constants.STATUS: err.status,
                    Constants.ERROR: err.error,
                    Constants.MESSAGE: err.message}
            
            return jsonify(failure_result),failure_result["status"]
            
        
    def add_user(self, user_data):
        """
        Registers a new manager user based on the provided user data.
        """
        try: 
            user = User(
            username = user_data["username"],
            password = user_data["password"],
            name = user_data["name"],
            phone = user_data["phone"],
            role = Constants.MANAGER
            )
            result = user.signup()
            if result is True:
                success_result = {
                        Constants.STATUS: 201,
                        Constants.MESSAGE: Constants.MANAGER_ADDED_MSG
                    }
                return jsonify(success_result),success_result["status"]
                
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            failure_result = {Constants.STATUS: err.status,
                    Constants.ERROR: err.error,
                    Constants.MESSAGE: err.message}
            
            return jsonify(failure_result),failure_result["status"]