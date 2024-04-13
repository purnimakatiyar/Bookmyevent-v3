"""This module provides functionality for user authentication including login, token refreshing,
and role retrieval."""
import logging
import pymysql
from models.database import DBConnection
from settings.config import queries
from passlib.hash import pbkdf2_sha256
from utils.exceptions import CustomException, DBException
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token, get_jti
from businesslogic.user_business import User
from settings.constants import Constants
logger = logging.getLogger("auth_business")


class Authenticate:
    
    """
    Authenticate class provides methods for user authentication including login, token refreshing,
    and role retrieval.
    """
    
    def __init__(self, **auth_details) -> None:
        
        """
        Initialize the Authenticate class with authentication details.
        """
        
        self.username = auth_details.get('username')
        self.password = auth_details.get('password')
        self.db = DBConnection()

    
    def login(self):
        
        """
        Authenticate user based on provided username and password.
        """
        
        try:
            user = User(username = self.username)
            result = user.check_user()
         
            if result is not None:
                user_password = self.get_password(self.username)
                role = self.get_role()
                if user_password[0] and pbkdf2_sha256.verify(self.password, user_password[0]):
                    access_token = create_access_token(identity=self.username, fresh=True)
                    refresh_token = create_refresh_token(identity=self.username)
                    user = User()
                    user_id = user.get_user_id(self.username)
                    self.db.insert_item(queries["INSERT_TOKEN_DETAILS"],
                             (user_id, get_jti(access_token), get_jti(refresh_token), Constants.ACTIVE))
                    response = {'role': role, Constants.ACCESS_TOKEN: access_token, Constants.REFRESH_TOKEN: refresh_token}
                    return response
                    
                else:
                    raise CustomException(401, Constants.INVALID_CREDENTIALS, Constants.WRONG_CREDENTIALS_MSG)
            else:
                raise CustomException(404, Constants.DOES_NOT_EXIST, Constants.USER_NOT_EXIST_MSG)
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
    
    
    def refresh_token(self):
        
        """
        Refresh the JWT token for the current user.
        """
        
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {Constants.ACCESS_TOKEN: new_token}
    
    
    def get_password(self, username):
        
        """
        Retrieve hashed password for the given username.
        """
        return self.db.get_item(queries["SEARCH_PASSWORD_IN_AUTHENTICATE"], (username,))
        
        
    def get_role(self) ->str:
        """
        Retrieve the role associated with the current user.
        """
        try:
            result = self.db.get_item(queries["SEARCH_ROLE_IN_AUTHENTICATE"], (self.username,))
            return result[0]
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
