"""
This module provides functionality for handling removing events-related requests in the application.
"""

import logging
from businesslogic.event_business import Event
from utils.exceptions import DBException, CustomException
from settings.constants import Constants 
from flask import jsonify
logger = logging.getLogger('remove_event_controller')


class RemoveEventController:
        
    """
    RemoveEventController class provides methods for handling removing events-related requests.
    """
    
    def remove_event(self, user_id, event_id):
        """
        Remove an event.
        """
        try:
            event = Event(user_id = user_id)
            result = event.remove_event(event_id)
            if result is not None:
                success_result = {
                    Constants.STATUS: 200,
                    Constants.MESSAGE: Constants.REMOVED_EVENT_MSG
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
            
          