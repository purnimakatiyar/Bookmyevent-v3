"""
This module provides functionality for handling viewing booked events-related requests in the application.
"""
import logging
from utils.exceptions import CustomException, DBException
from businesslogic.book_events_business import BookEvents
from settings.constants import Constants 
from flask import jsonify
logger = logging.getLogger('view_booked_event_controller')

class ViewBookEventsController:
    """
    ViewBookEventsController: Provides methods for handling viewing booked events-related requests.
    """
    
    def booked_events_list_to_dict(self, events):
        """
        Convert booked events list to dictionary format.
        """
        result_list = []
        for event in events:
            booking_id, user_id, event_id, event_name, event_date, ticket_qty = event
            event_dict = {  Constants.BOOKING_ID : booking_id,
                            Constants.EVENT_NAME: event_name,
                            Constants.EVENT_DATE: event_date,
                            # Constants.LOCATION: location,
                            # Constants.PRICE: price,
                            # Constants.CATEGORY: category,
                            Constants.TICKET_QTY: ticket_qty
                        }
            result_list.append(event_dict)
        return result_list
    
    
    def view_booked_event(self, user_id):
        """
        View booked events for a user.
        """
        try:
            booked_events = BookEvents()
            result = booked_events.view_booked_event(user_id) 
            if result is not None:
                response = self.booked_events_list_to_dict(result)
                success_result = {Constants.STATUS: 200, Constants.BOOKED_EVENTS: response}
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