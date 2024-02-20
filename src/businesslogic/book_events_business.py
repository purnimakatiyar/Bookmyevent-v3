"""
BookEvents class provides methods for booking events, 
managing ticket quantities, and viewing booked events.
"""
import logging
from settings.config import queries
from models.database import DBConnection
from utils.uuid_generator import generate_uuid
from utils.exceptions import CustomException, DBException
from businesslogic.event_business import Event
from settings.constants import Constants
import pymysql

logger = logging.getLogger('book_event_business')

class BookEvents:
    
    
    def __init__(self, **kwargs: dict) -> None: 
        """
        Initialize the BookEvents class with booking details.
        """
        self.booking_id = generate_uuid()
        self.user_id = kwargs.get('user_id')
        self.event_id = kwargs.get('event_id')
        self.ticket_quantity = kwargs.get('ticket_quantity')
        self.db = DBConnection()
        

    def get_ticket_qty(self, event_id):
        """
        Method to get the ticket quantity
        """
        return self.db.get_item(queries["GET_TICKET_QTY"], (event_id,))
        
       
        
    def book_event(self, user_id, request_data) ->None:
        """
        Method to book the event for customer
        """
        
        try:
            event = Event().get_event_by_id(self.event_id)
            
            if event is None:
                raise CustomException(404, Constants.DOES_NOT_EXIST, Constants.EVENT_NOT_EXISTS_MSG)
            else:
                if self.update_ticket(request_data, self.event_id):
                    booking_id = generate_uuid()
                    booked_event_details = (booking_id, user_id, self.event_id, event[2], event[3], request_data)
                    self.db.insert_item(queries["INSERT_BOOKING"], booked_event_details)
                    return True
                    
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
        
        
    def update_ticket(self, tickets , event_id) ->None:
        """
        Method to update the tickets of the event which is booked
        """
        
        try:
            event_obj = Event()
            current_ticket_qty = self.get_ticket_qty(event_id)
            if current_ticket_qty is not None:
                if int(tickets) > current_ticket_qty[0]:  
                    raise CustomException(422, Constants.UNPROCESSABLE_ENTITY, Constants.NOT_AVAILABLE_TICKETS_MSG)
                else:
                    get_event_detail = event_obj.get_event_by_id(event_id)
                    print(get_event_detail)
                    event_id = get_event_detail[0]
                    updated_ticket_qty = current_ticket_qty[0] - int(tickets)
                    self.db.update_item(queries["UPDATE_TICKET_QTY"], (updated_ticket_qty, event_id,))
                    return True
            else:
                raise CustomException(404, Constants.NOT_FOUND, Constants.NO_TICKETS_MSG)
            
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
            
            
    def view_booked_event(self, user_id):
        
        """
        Method to view booked events for a user
        """
        
        try:
            booked_events = self.db.get_items(queries["GET_BOOKED_EVENTS"], (user_id,))
            if booked_events is not None:
                return booked_events
            else:
                raise CustomException(404, Constants.NOT_FOUND, Constants.NO_BOOKED_EVENT_MSG)
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
            