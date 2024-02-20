"""
This module provides functionality for handling adding events-related requests in the application.
"""
import logging
from settings.config import prompts
from businesslogic.user_business import User
from businesslogic.event_business import Event
from utils.exceptions import CustomException, DBException
from settings.constants import Constants 
from flask import jsonify
logger = logging.getLogger('add_event_controller')


class AddEventController:
    """
    AddEventController class provides methods for handling adding events-related requests
    """
    def __init__(self):
        """
        Initialize AddEventController with Event and User instances.
        """
        self.event = Event()
        self.user = User()
        
        

    def add_event(self, user_id, event_data) ->None:
        """
        Add an event.
        """
        try:
           
            event = Event(
            user_id = user_id,
            event_name = event_data["event_name"],
            event_date = event_data["event_date"],
            location = event_data["location"],
            price = event_data["price"],
            category = event_data["category"],
            ticket_quantity = event_data["ticket_qty"]
            )
            event.add_event()
            success_result = {
                        Constants.STATUS: 201,
                        Constants.MESSAGE: Constants.EVENT_ADDED_MSG
                    }
            return jsonify(success_result),success_result["status"]
            
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            failure_result = {Constants.STATUS: err.status,
                    Constants.ERROR: err.error,
                    Constants.MESSAGE : err.message}
            
            return jsonify(failure_result),failure_result["status"]