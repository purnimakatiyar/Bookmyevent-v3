"""
This module provides functionality for managing JWT tokens including checking if a token is revoked and revoking a token.
"""
import logging
from models.database import DBConnection
from settings.config import queries
from settings.constants import Constants
from utils.exceptions import DBException
from settings.constants import Constants
import pymysql

logger = logging.getLogger('logout_business')

class Token:
    
    
    @staticmethod
    def check_token_revoked(jwt_payload):
        """check if token is revoked or not"""
        jti_access_token = jwt_payload.get('jti')

        result = DBConnection().get_item(queries["GET_TOKEN_STATUS"], (jti_access_token,))[0]
        if result == Constants.REVOKED:
            return True
        return False

    @staticmethod
    def revoke_token(jwt_payload):
        """To change the status of token to revoked"""
        try:
            jti_access_token = jwt_payload["jti"]

            DBConnection().update_item(queries["UPDATE_TOKEN_STATUS"], (Constants.REVOKED, jti_access_token,))
            return
            
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, Constants.INTERNAL_SERVER_ERROR, Constants.INTERNAL_SERVER_ERROR_MSG)
              