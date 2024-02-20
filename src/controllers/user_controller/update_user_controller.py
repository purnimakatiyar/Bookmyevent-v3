"""
This module contains the UpdateUserController class, which handles requests related to updating user information in a Flask application.
"""
import logging
from utils.exceptions import DBException, CustomException
from businesslogic.user_business import User
from settings.constants import Constants 
from flask import jsonify
logger = logging.getLogger('update_user_controller')

class UpdateUserController:
    """
    UpdateUserController class Handles user information update operations.
    """


    def update_user_details(self,user_id, user_data):
        """Method to update the user details"""
              
        try:
            user = User(user_id = user_id)
            if user_data["name"] is not None:
                user.update_user_name(user_data["name"])
            if user_data["password"] is not None:
                user.update_user_phone(user_data["password"])
            if user_data["phone"] is not None:
                user.update_user_phone(user_data["phone"])
                
            success_result = {
                Constants.STATUS: 200, 
                Constants.MESSAGE: Constants.UPDATE_DETAILS_MSG
            }
            return jsonify(success_result),success_result["status"]
        
        except (DBException, CustomException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            failure_result = {Constants.STATUS: err.status,
                    Constants.ERROR: err.error,
                    Constants.MESSAGE: err.message}
            return jsonify(failure_result),failure_result["status"]
             
    

    # def update_user_name(self, user_id, name):
    #     """
    #     Updates the name of the user with the specified user ID.
    #     """
    #     try:
    #         user = User(user_id)
    #         result = user.update_user_name(name)
    #         if result is True:
    #             success_result = {
    #                 Constants.STATUS: 200, 
    #                 Constants.MESSAGE: Constants.UPDATE_NAME_MSG
    #             }
    #             return jsonify(success_result),success_result["status"]
            
    #     except (CustomException, DBException) as err:
    #         if isinstance(err, CustomException):
    #             logger.error("Custom error handled {}".format(err.error))
    #         failure_result = {Constants.STATUS: err.status,
    #                 Constants.ERROR: err.error,
    #                 Constants.MESSAGE: err.message}
    #         return jsonify(failure_result),failure_result["status"]
            
        
    # def update_user_password(self, user_id, password):
    #     """
    #     Updates the password of the user with the specified user ID.
    #     """
    #     try:
    #         user = User(user_id)
    #         result = user.update_user_password(password)
    #         if result is True:
    #             success_result = {
    #                 Constants.STATUS: 200, 
    #                 Constants.MESSAGE: Constants.UPDATE_PASSWORD_MSG
    #             }
    #             return jsonify(success_result),success_result["status"]
            
    #     except (DBException,CustomException) as err:
    #         if isinstance(err, CustomException):
    #             logger.error("Custom error handled {}".format(err.error))
    #         failure_result = {Constants.STATUS: err.status,
    #                 Constants.ERROR: err.error,
    #                 Constants.MESSAGE : err.message}
    #         return jsonify(failure_result),failure_result["status"]
        
        
    # def update_user_phone(self, user_id, phone): 
    #     """
    #     Updates the phone number of the user with the specified user ID.
    #     """
    #     try:
    #         user = User(user_id)
    #         result = user.update_user_phone(phone)
    #         if result is True:
    #             success_result = {
    #                 Constants.STATUS: 200, 
    #                 Constants.MESSAGE: Constants.UPDATE_PHONE_MSG
    #             }
    #             return jsonify(success_result),success_result["status"]
            
    #     except (DBException, CustomException) as err:
    #         if isinstance(err, CustomException):
    #             logger.error("Custom error handled {}".format(err.error))
    #         failure_result = {Constants.STATUS: err.status,
    #                 Constants.ERROR: err.error,
    #                 Constants.MESSAGE: err.message}
    #         return jsonify(failure_result),failure_result["status"]
             
                
