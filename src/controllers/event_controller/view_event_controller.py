"""
"""
"""
This module contains the ViewEventController class, which is responsible for handling requests related to viewing events in a Flask application.
"""

import logging
from settings.config import prompts
from businesslogic.user_business import User
from businesslogic.event_business import Event
from utils.exceptions import CustomException, DBException
from settings.constants import Constants 
from flask import jsonify
logger = logging.getLogger('view_event_controller')


class ViewEventController:
    """
    ViewEventController class Handles various operations related to viewing events, including fetching event details, listing events, listing all events, filtering events, and searching events.
    """
    
    def __init__(self):
        self.event = Event()
        self.user = User()
       
        
    def events_list_to_dict(self, events):
        """
        Converts a list of event details into a dictionary format suitable for JSON response.
        """
        
        result_list = []
        for event in events:
            event_id, user_id, event_name, event_date, location, price, category, ticket_qty = event
            event_dict = {  "event_id": event_id,
                            Constants.EVENT_NAME: event_name,
                            Constants.EVENT_DATE: event_date,
                            Constants.LOCATION: location,
                            Constants.PRICE: price,
                            Constants.CATEGORY: category,
                            Constants.TICKET_QTY: ticket_qty
                        }
            result_list.append(event_dict)
        return {Constants.STATUS: 200, Constants.EVENTS: result_list}
        
        
    def view_event(self, event_id):
        
        """
        Retrieves and returns details of a specific event identified by its ID.
        """
        try:
            event = Event(event_name = event_id)
            event_details = event.get_event_by_id(event_id)
            for event_data in event_details:
                success_result = {Constants.EVENT_NAME: event_data[0],
                        Constants.EVENT_DATE: event_data[1],
                        Constants.LOCATION: event_data[2],
                        Constants.PRICE: event_data[3],
                        Constants.CATEGORY: event_data[4],
                        Constants.TICKET_QTY: event_data[5]
                        }
                return jsonify(success_result),success_result["status"]
                
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            failure_result = {Constants.STATUS: err.status,
                    Constants.ERROR: err.error,
                    Constants.MESSAGE: err.message}
            return jsonify(failure_result),failure_result["status"]
            
          
    def list_events(self, username):
        """
        Retrieves and returns a list of events associated with a specific user identified by their username.
        """
        
        try:
            user_id = self.user.get_user_id(username)
            event = Event(user_id = user_id)
            events = event.list_events()
            success_result = self.events_list_to_dict(events)
            return jsonify(success_result),success_result["status"]
        
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            failure_result = {Constants.STATUS: err.status,
                    Constants.ERROR: err.error,
                    Constants.MESSAGE: err.message}
            return jsonify(failure_result),failure_result["status"]
        
        
    def list_all_events(self):
        """
        Retrieves and returns a list of all events in the system.
        """
        
        try:
            events = self.event.list_all_events()
            success_result = self.events_list_to_dict(events)
            return jsonify(success_result),success_result["status"]
        
        
        except (DBException, CustomException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            failure_result = {Constants.STATUS: err.status,
                    Constants.ERROR: err.error,
                    Constants.MESSAGE: err.message}
            return jsonify(failure_result),failure_result["status"]
            
        
    def filter_event(self, event_data):
        """
        Filters events based on specific criteria provided in event_data.
        """
        
        try:
            if event_data["price"] is not None:
                events = self.event.filter_event_by_price(event_data["price"])
            if event_data["category"] is not None:
                events = self.event.filter_event_by_category(event_data["category"])
            if event_data["location"] is not None:
                events = self.event.filter_event_by_location(event_data["location"])
            
            success_result = self.events_list_to_dict(events)
            return jsonify(success_result),success_result["status"]
                    
        except (DBException, CustomException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            failure_result = {Constants.STATUS: err.status,
                    Constants.ERROR: err.error,
                    Constants.MESSAGE: err.message}
            return jsonify(failure_result),failure_result["status"]
            
            
    def search_event(self, event_data):
        """
        Searches for events based on keywords provided in event_data.
        """
        
        try:
            events = self.event.search_event(event_data)
            success_result = self.events_list_to_dict(events)
            return jsonify(success_result),success_result["status"]
            
        except (DBException, CustomException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            failure_result = {Constants.STATUS: err.status,
                    Constants.ERROR: err.error,
                    Constants.MESSAGE: err.message}
            return jsonify(failure_result),failure_result["status"]   
