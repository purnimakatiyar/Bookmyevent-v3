import pymysql
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger('database')

dotenv_path = Path('.env')

load_dotenv(dotenv_path = dotenv_path)
host=os.getenv('DB_HOST')
user=os.getenv('DB_USERNAME')
password=os.getenv('DB_PASSWORD')
database=os.getenv('DB_NAME')
port=int(os.getenv('DB_PORT'))

class DBConnection:

    def __init__(self):
        try:
            self.mydb = pymysql.connect(
                
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,

            )
            self.cursor = self.mydb.cursor()
        except Exception as err:
            logger.exception(err)
        else:
            logger.debug("DB Connection created")
              
            
    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mydb.commit()
        self.mydb.close()

    
    def get_item(self, query, data):
        
        with DBConnection() as cursor:
            try:
                cursor.execute(query, data)
                response = cursor.fetchone()
            except pymysql.Error as error:
                print(error)
                # logger.exception(error)
                raise pymysql.Error
            
            return response
    
    
    def get_items(self, query, data):
        
        with DBConnection() as cursor:
            try:
                cursor.execute(query, data)
                response = cursor.fetchall()
            except pymysql.Error as error:
                print(error)
                # logger.exception(error)
                raise pymysql.Error
            return response
        
    
    def get_all_items(self, query):
        events = None
        with DBConnection() as cursor:
            try:
                cursor.execute(query)
                events = cursor.fetchall()
            except pymysql.Error:
                # print(error)
                # logger.exception(error)
                raise pymysql.Error
            return events

    
    def insert_item(self, query, data):
        with DBConnection() as cursor:
            try:
                cursor.execute(query, data)
                
            except pymysql.Error as error:
                print(error)
                # logger.exception(error)
                raise pymysql.Error

    
    def update_item(self, query, data):
        with DBConnection() as cursor:
            try:
                cursor.execute(query, data)
             
            except pymysql.Error:
                # print(error)
                # logger.exception(error)
                raise pymysql.Error
             
         
    def delete_item(self, query, data):
        with DBConnection() as cursor:
            try:
                cursor.execute(query, data)
             
            except pymysql.Error as error:
                print(error)
                # logger.exception(error)
                raise pymysql.Error
            

db = DBConnection()


# import os
# import pymysql
# import logging
# from dotenv import load_dotenv
# load_dotenv()
# logger = logging.getLogger('database')


# class DBConnection:

#     def __init__(self):
#         try:
#             self.mydb = pymysql.connect(
#                 host=os.getenv('DB_HOST'),
#                 user=os.getenv('DB_USERNAME'),
#                 password=os.getenv('DB_PASSWORD'),                           
#                 database=os.getenv('DB_NAME'),
#                 port=int(os.getenv('DB_PORT'))
#             )
#             self.cursor = self.mydb.cursor()
#         except Exception as err:
#             logger.exception(err)
#         else:
#             logger.debug("DB Connection created")
              
            
#     def __enter__(self):
#         return self.cursor

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.mydb.commit()
#         self.mydb.close()

    
#     def get_item(self, query, data):
        
#         with DBConnection() as cursor:
#             try:
#                 cursor.execute(query, data)
#                 response = cursor.fetchone()
#             except mysql.connector.Error as error:
#                 print(error)
#                 # logger.exception(error)
#                 raise mysql.connector.Error
            
#             return response
    
    
#     def get_items(self, query, data):
        
#         with DBConnection() as cursor:
#             try:
#                 cursor.execute(query, data)
#                 response = cursor.fetchall()
#             except mysql.connector.Error as error:
#                 print(error)
#                 # logger.exception(error)
#                 raise mysql.connector.Error
#             return response
        
    
#     def get_all_items(self, query):
#         events = None
#         with DBConnection() as cursor:
#             try:
#                 cursor.execute(query)
#                 events = cursor.fetchall()
#             except mysql.connector.Error:
#                 # print(error)
#                 # logger.exception(error)
#                 raise mysql.connector.Error
#             return events

    
#     def insert_item(self, query, data):
#         with DBConnection() as cursor:
#             try:
#                 cursor.execute(query, data)
                
#             except mysql.connector.Error as error:
#                 print(error)
#                 # logger.exception(error)
#                 raise mysql.connector.Error

    
#     def update_item(self, query, data):
#         with DBConnection() as cursor:
#             try:
#                 cursor.execute(query, data)
             
#             except mysql.connector.Error:
#                 # print(error)
#                 # logger.exception(error)
#                 raise mysql.connector.Error
             
         
#     def delete_item(self, query, data):
#         with DBConnection() as cursor:
#             try:
#                 cursor.execute(query, data)
             
#             except mysql.connector.Error as error:
#                 print(error)
#                 # logger.exception(error)
#                 raise mysql.connector.Error
            

# db = DBConnection()