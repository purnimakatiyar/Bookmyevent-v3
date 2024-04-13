"""
This module provides functionality for managing events including adding, removing, updating, and searching events.
"""
import logging
from settings.config import queries
from utils import uuid_generator
from utils.uuid_generator import generate_uuid
from models.database import DBConnection
from utils.exceptions import CustomException, DBException
from settings.constants import Constants
import pymysql
logger = logging.getLogger('event_business')


class Event:
    
    """
    Event class provides methods for managing events.
    """
   
    def __init__(self, **event_details: dict) -> None:
        """
        Initialize the Event class with event details.
        """
        self.event_id = generate_uuid()
        self.user_id = event_details.get('user_id')
        self.event_name = event_details.get('event_name')
        self.event_date = event_details.get('event_date')
        self.location = event_details.get('location')
        self.price = event_details.get('price')
        self.category = event_details.get('category')
        self.ticket_quantity = event_details.get('ticket_quantity')
        self.db = DBConnection()
      
    
    def check_event_by_id(self, event_id):
        """
        Method to check if event exists
        """
        
        result = self.db.get_item(queries["SEARCH_EVENT_BY_ID"],  (event_id,))
        if result is not None:
            return True
        else:
            return False 
    
    
    def add_event(self) ->None:
        """
        Method to add event in the events table
        """
        try:
            event_details = (
                self.event_id,
                self.user_id,
                self.event_name,
                self.event_date,
                self.location,
                self.price,
                self.category,
                self.ticket_quantity
                )
            self.db.insert_item(queries["INSERT_EVENT"], event_details)  
            return True    
            
        except pymysql.Error as error:
            logger.error("{} occurred in Database".format(error))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
        
    def remove_event(self, event_id) -> None:
        """
        Method to remove event in the events table
        """
        try:
            
            event = self.check_event_by_id(event_id)
            if event is True:
                print(self.user_id)
                self.db.delete_item(queries["DELETE_EVENT"], (self.user_id, event_id,)) 
                return True   
            else:
                raise CustomException(404, Constants.DOES_NOT_EXIST, Constants.NO_EVENT_FOUND_MSG)
            
        except pymysql.Error as error:
            logger.error("{} occurred in Database".format(error))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
        
          
    def get_event_by_user(self):
        """
        Method to get the event by a particular manager
        """
        
        try:
            result = self.db.get_item(queries["SEARCH_EXISTING_EVENT"], (self.user_id, self.event_name,))
            if result is not None:
                return result
            elif result is None:
                raise CustomException(404, Constants.NOT_FOUND, Constants.NO_EVENTS_MSG)
            else:
                raise CustomException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_FETCH_ERROR_MSG)
        
        except pymysql.Error as error:
            logger.error("{} occurred in Database".format(error))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
        
    def get_event(self):
        """
        Method to get event by event name
        """
        try:
            result =  self.db.get_item(queries["SEARCH_EVENT"],  self.event_name)
            if result is not None:
                return result
            elif result is None:
                raise CustomException(404, Constants.NOT_FOUND, Constants.NO_EVENTS_MSG)
            
        
        except pymysql.Error as error:
            logger.error("{} occurred in Database".format(error))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
        
    def get_event_by_id(self, event_id):
        """
        Method to get event by event name
        """
        try:

            result =  self.db.get_item(queries["SEARCH_EVENT_BY_ID"],  (event_id,))
            if result is not None:
                return result
            elif result is None:
                raise CustomException(404, Constants.NOT_FOUND, Constants.NO_EVENTS_MSG)
            
        
        except pymysql.Error as error:
            logger.error("{} occurred in Database".format(error))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
    
    def list_all_events(self) ->list:
        """
        Method to list overall events from the events table
        """
        
        try:
            result = self.db.get_all_items(queries["LIST_EVENTS"])
            if result is not None:
                return result
            elif result is None:
                raise CustomException(404, Constants.NOT_FOUND, Constants.NO_EVENTS_MSG)
            
        
        except pymysql.Error as error:
            logger.error("{} occurred in Database".format(error))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
            
        
    def list_user_events(self) ->tuple:
        """
        Method to list the events particular to a manager for the manager itself
        """
        
        try:
            result = self.db.get_items(queries["LIST_USER_EVENTS"], (self.user_id,))
            if result is not None:
                return result
            elif result is None:
                raise CustomException(404, Constants.NOT_FOUND, Constants.NO_EVENTS_MSG)
           
        
        except pymysql.Error as error:
            logger.error("{} occurred in Database".format(error))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
            
              
    def filter_event_by_price(self, price: str) ->list:
        """
        Method to filter the events by price
        """
        
        try:
            print("HELLOOOOOOOOOOO")
            events = self.db.get_items(queries["FILTER_PRICE"], (price,))
            if events is not None:
                return events
            elif events is None:
                raise CustomException(404, Constants.NOT_FOUND, Constants.NO_EVENTS_MSG)
        
        except pymysql.Error as error:
            logger.error("{} occurred in Database".format(error))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
       
        
    def filter_event_by_category(self, category):
        
        """
        Method to filter the events by category
        """
        try:
            events = self.db.get_items(queries["FILTER_CATEGORY"], (category,))
            if events is not None:
                return events
            elif events is None:
                raise CustomException(404, Constants.NOT_FOUND, Constants.NO_EVENTS_MSG)
            
        except pymysql.Error as error:
            logger.error("{} occurred in Database".format(error))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
        
    def filter_event_by_location(self, location):
        """
        Method to filter the events by location
        """
        try:
            events = self.db.get_items(queries["FILTER_LOCATION"], (location,))
            if events is not None:
                return events
            elif events is None:
                raise CustomException(404, Constants.NOT_FOUND, Constants.NO_EVENTS_MSG)
            
        except pymysql.Error as error:
            logger.error("{} occurred in Database".format(error))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
          
    def search_event(self, partial_name: str) ->list:
        """
        Method to search the event by entering name partially or completely
        """
        
        try:
            partial_name = f"%{partial_name}%"
            events = self.db.get_items(queries["SEARCH_BY_EVENT_NAME"], (partial_name,))
            if events is not None:
                return events
            elif events is None:
                raise CustomException(404, Constants.NOT_FOUND, Constants.NO_EVENTS_MSG)

        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
        

    def update_event_name(self, event_id, event_name) ->None:
        """
        Method to update the event details by the manager
        """
        try:
            
            if  self.check_event_by_id(event_id) is True:
                result = self.db.update_item(queries["UPDATE_EVENT_NAME"],
                    (event_name, event_id, self.user_id,))
                if result is True:
                    return result
                
            else:
                raise CustomException(404, Constants.DOES_NOT_EXIST, Constants.NO_EVENT_EXIST_MSG)
       
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
        

    def update_event_date(self, event_id, event_date) ->None:
        """
        Method to update the event date
        """
        
        try: 
            if self.check_event_by_id(event_id) is True: 
                result = self.db.update_item(
                    queries["UPDATE_EVENT_DATE"],
                    (event_date, event_id, self.user_id))
                if result is True:
                    return result
                
            else:
                raise CustomException(404, Constants.DOES_NOT_EXIST, Constants.NO_EVENT_EXIST_MSG)
        
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
    

    def update_event_location(self, event_id, location):
        try: 
            if self.check_event_by_id(event_id) is True: 
                result = self.db.update_item(
                    queries["UPDATE_EVENT_LOCATION"],
                    (event_date, event_id, self.user_id))
                if result is True:
                    return result
                
            else:
                raise CustomException(404, Constants.DOES_NOT_EXIST, Constants.NO_EVENT_EXIST_MSG)
        
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
        
    def update_event_price(self, event_id, price):
        
        """
        Method to update the event location
        """
        try: 
            if self.check_event_by_id(event_id) is True: 
                result = self.db.update_item(
            queries["UPDATE_EVENT_PRICE"],
                (price, event_id, self.user_id))
                if result is True:
                    return result
                
            else:
                raise CustomException(404, Constants.DOES_NOT_EXIST, Constants.NO_EVENT_EXIST_MSG)
        
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
        

    def update_event_category(self, event_id, category):
        """
        Method to update the event category
        """
        try: 
            if self.check_event_by_id(event_id) is True: 
                result = self.db.update_item(
                queries["UPDATE_EVENT_CATEGORY"],
                (category, event_id, self.user_id))
                if result is True:
                    return result
            else:
                raise CustomException(404, Constants.DOES_NOT_EXIST, Constants.NO_EVENT_EXIST_MSG)
        
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
