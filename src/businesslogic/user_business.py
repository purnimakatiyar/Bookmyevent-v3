"""
This module provides functionality for managing user accounts including signup, login, profile management, and access control.
"""
import logging
from settings.config import queries
from models.database import DBConnection
from passlib.hash import pbkdf2_sha256
from utils.uuid_generator import generate_uuid
from utils.exceptions import CustomException, DBException
from settings.constants import Constants
import pymysql
logger = logging.getLogger('user_business')


class User:
    
    """
    User class provides methods for managing user accounts.
    """
    
    def __init__(self, **user_details: dict) ->None:
        """
        Initialize the User class with user details.
        """
        self.uuid = generate_uuid()
        self.user_id = user_details.get('user_id')
        self.username = user_details.get('username')
        self.password = user_details.get('password')
        self.name = user_details.get('name')
        self.phone = user_details.get('phone')
        self.role = user_details.get('role')
        self.db = DBConnection()
       
        
    def check_user(self) -> None:
        
        """
        Check if a user exists in the database.
        """
        return self.db.get_item(queries["SEARCH_EXIST_USER_IN_AUTHENTICATE"], (self.username,))
    
    def check_manager(self, username) -> None:
        """
        Check if a manager exists in the database.
        """
        return self.db.get_item(queries["SEARCH_EXIST_USER_IN_AUTHENTICATE"], (username,))
    
    
    def signup(self):  
        """
        Register a new user.
        """
        try:
            if self.check_user():
                raise CustomException(409, Constants.ALREADY_EXISTS, Constants.USER_ALREADY_EXISTS_MSG)
            else:
                return self.save_info()
                
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
        
    def save_info(self):
        """
        Save user information to the database.
        """
        try:
            hashed_password = pbkdf2_sha256.hash(self.password)
            auth_details = (
                self.uuid,
                self.username,
                hashed_password,
                self.role
                )
            user_details = (
                self.uuid,
                self.username, 
                self.name,
                self.phone,
                )
            self.db.insert_item(queries["INSERT_INTO_AUTHENTICATE"], auth_details)
            self.db.insert_item(queries["INSERT_USERDETAILS"], user_details)
            return True
            
           
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
        
            
    def get_user(self, username):
        """
        Get user information by username.
        """
        return self.db.get_item(queries["SEARCH_EXIST_USER_IN_AUTHENTICATE"], (username,))
    
    def remove_manager(self, username: str) ->None:
        """
        Remove a manager from the system.
        """
        try:
            if self.check_manager(username) is not None:
                self.db.delete_item(queries["DELETE_USERDETAILS"], (username,))
                self.db.delete_item(queries["DELETE_FROM_AUTHENTICATE"], (username,))
                
            else:
                raise CustomException(404, Constants.DOES_NOT_EXIST, Constants.MANAGER_NOT_FOUND_MSG)
        
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
              
    def get_user_id(self, username: str) -> str:
        """
        Get the user ID of a user.
        """
        return self.db.get_item(queries["SEARCH_USER_ID_IN_USERDETAILS"], (username,))[0]
    
    def list_all_managers(self):
        """
        List all managers in the system.
        """
        try:
            result = self.db.get_items(queries["SEARCH_MANAGER"], ("Manager",))
            if result is not None:
                return result
            elif result is None:
                raise CustomException(404, "NotFound", "No content found while searching.")
           
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
        
    def view_profile(self, user_id):
        """
        View user profile information.
        """
        try:
            result = self.db.get_item(queries["SEARCH_USER_IN_USERDETAILS"], (user_id,))
            if result is not None:
                return result
            elif result is None:
                raise CustomException(404, Constants.NOT_FOUND, Constants.NO_CONTENT_MSG)
            
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
    
    def update_user_name(self, new_name)-> None:
        """
        Update user's name.
        """
        try:
            self.db.update_item(queries["UPDATE_NAME"], (new_name, self.user_id))
            
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
        
      
    def update_user_password(self, new_password = None):
        """
        Update user's password.
        """
        try:
            password = pbkdf2_sha256.hash(new_password)
            self.db.update_item(queries["UPDATE_PASSWORD"], (password, self.user_id))
           
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
    
    def update_user_phone(self, new_phone = None):
        """
        Update user's phone number.
        """
        try:
            self.db.update_item(queries["UPDATE_PHONE"], (new_phone, self.user_id))
            
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              
