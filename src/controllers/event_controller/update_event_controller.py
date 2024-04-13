"""
This module provides functionality for handling update event-related requests in the application.
"""
import logging
from businesslogic.user_business import User
from businesslogic.event_business import Event
from utils.exceptions import CustomException, DBException
from settings.constants import Constants 
from flask import jsonify
logger = logging.getLogger('update_event_controller')


class UpdateEventController:
    """
    UpdateEventController class provides methods for handling update event-related requests.
    """
    
    def __init__(self):
        """
        Initialize UpdateEventController with instances of Event and User classes.
        """
        self.event = Event()
        self.user = User()
        
        
    def update_event_details(self, user_id, event_id, event_data):
        """Method to update the user details"""
              
        try:
            print(user_id, event_id, event_data)
            event = Event(user_id = user_id, event_id = event_id)
            if event_data["event_name"] is not None:
                event.update_event_name(event_id, event_data["event_name"])
            if event_data["event_date"] is not None:
                event.update_event_date(event_id, event_data["event_date"])
            if event_data["price"] is not None:
                event.update_event_price(event_id, event_data["price"])
            if event_data["category"] is not None:
                event.update_event_category(event_id, event_data["category"])
            if event_data["location"] is not None:
                event.update_event_location(event_id, event_data["location"])
            if event_data["ticket_qty"] is not None:
                event.update_event_ticket_qty(event_id, event_data["ticket_qty"])
            
                
            success_result = {
                Constants.STATUS: 200, 
                Constants.MESSAGE: Constants.UPDATE_EVENT_MSG
            }
            return jsonify(success_result),success_result["status"]
        
        except (DBException, CustomException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            failure_result = {Constants.STATUS: err.status,
                    Constants.ERROR: err.error,
                    Constants.MESSAGE: err.message}
            return jsonify(failure_result),failure_result["status"]
             
             
    # def update_event_name(self, event_id, event_name, user_id):
    #     """
    #     Update the name of an event.
    #     """
        
    #     try:
    #         event = Event(user_id = user_id, event_id = event_id)
    #         event.update_event_name(event_name)
            
    #         success_result = {
    #             Constants.STATUS: 200,
    #             Constants.MESSAGE: Constants.UPDATE_EVENT_NAME_MSG
    #         }
    #         return jsonify(success_result),success_result["status"]
            
    #     except (CustomException, DBException) as err:
    #         if isinstance(err, CustomException):
    #             logger.error("Custom error handled {}".format(err.error))
    #         failure_result = {
    #             Constants.STATUS: err.status,
    #             Constants.ERROR: err.error,
    #             Constants.MESSAGE: err.message
    #         }
            
    #         return jsonify(failure_result),failure_result["status"]
           
           
    # def update_event_date(self, event_id, event_date, user_id):
    #     """
    #     Update the date of an event.
    #     """
        
    #     try:
    #         event = Event(user_id = user_id, event_id = event_id)
    #         event.update_event_date(event_date)
            
    #         success_result = {
    #             Constants.STATUS: 200,
    #             Constants.MESSAGE: Constants.UPDATE_EVENT_DATE_MSG
    #         }
    #         return jsonify(success_result),success_result["status"]
            
    #     except (CustomException, DBException) as err:
    #         if isinstance(err, CustomException):
    #             logger.error("Custom error handled {}".format(err.error))
    #         failure_result = {
    #             Constants.STATUS: err.status,
    #             Constants.ERROR: err.error,
    #             Constants.MESSAGE: err.message
    #         }
    #         return jsonify(failure_result),failure_result["status"]
        
        
    # def update_event_price(self, event_id, price, user_id):
    #     """
    #     Update the price of an event.
    #     """
        
    #     try:
    #         event = Event(user_id = user_id, event_id = event_id)
    #         event.update_event_price(price)
           
    #         success_result = {
    #             Constants.STATUS: 200,
    #             Constants.MESSAGE: Constants.UPDATE_EVENT_PRICE_MSG
    #         }
    #         return jsonify(success_result),success_result["status"]
            
    #     except (CustomException, DBException) as err:
    #         if isinstance(err, CustomException):
    #             logger.error("Custom error handled {}".format(err.error))
    #         failure_result = {
    #             Constants.STATUS: err.status,
    #             Constants.ERROR: err.error,
    #             Constants.MESSAGE: err.message
    #         }
    #         return jsonify(failure_result),failure_result["status"]
        
        
    # def update_event_category(self, event_id, category, user_id):
    #     """
    #     Update the category of an event.
    #     """
        
    #     try:
    #         event = Event(user_id = user_id, event_id = event_id)
    #         event.update_event_category(category)
            
    #         success_result = {
    #             Constants.STATUS: 200,
    #             Constants.MESSAGE: Constants.UPDATE_EVENT_CATEGORY_MSG
    #         }
    #         return jsonify(success_result),success_result["status"]
            
    #     except (CustomException, DBException) as err:
    #         if isinstance(err, CustomException):
    #             logger.error("Custom error handled {}".format(err.error))
    #         failure_result = {
    #             Constants.STATUS: err.status,
    #             Constants.ERROR: err.error,
    #             Constants.MESSAGE: err.message
    #         }
    #         return jsonify(failure_result),failure_result["status"]
            
            
    # def update_event_location(self, event_id, location, user_id):
    #     """
    #     Update the location of an event.
    #     """
        
    #     try:
    #         event = Event(user_id = user_id, event_id = event_id)
    #         event.update_event_location(location)
            
    #         success_result = {
    #             Constants.STATUS: 200,
    #             Constants.MESSAGE: "Updated event category successfully."
    #         }
    #         return jsonify(success_result),success_result["status"]
                
    #     except (CustomException, DBException) as err:
    #         if isinstance(err, CustomException):
    #             logger.error("Custom error handled {}".format(err.error))
    #         failure_result = {
    #             Constants.STATUS: err.status,
    #             Constants.ERROR: err.error,
    #             Constants.MESSAGE: err.message
    #         }
    #         return jsonify(failure_result),failure_result["status"]
            
           
    
    
