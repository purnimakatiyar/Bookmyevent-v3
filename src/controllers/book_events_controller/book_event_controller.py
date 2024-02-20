"""
This module provides functionality for handling booking events-related requests in the application.
"""
import logging
from businesslogic.book_events_business import BookEvents
from utils.exceptions import CustomException, DBException
from settings.constants import Constants 
from flask import jsonify
logger = logging.getLogger('book_event_controller')

class BookEventsController:
    """
    BookEventsController class provides methods for handling booking events-related requests.
    """
    
    def book_event(self, event_id, user_id, request_data) ->None:
        """
        Book an event for a customer.
        """
        
        try:
            
            event_obj = BookEvents(event_id = event_id)
            result = event_obj.book_event(user_id, request_data)
            if result is True:
                success_result = {
                    Constants.STATUS: 201,
                    Constants.MESSAGE: Constants.BOOKED_EVENT_MSG
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