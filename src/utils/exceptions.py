class MyExceptions(Exception):
    
    def __init__(self, status, error, message):
        self.status = status
        self.error = error
        self.message = message
        

        
class CustomException(MyExceptions):
    pass
    
class DBException(MyExceptions):
    pass

# class AlreadyExists(CustomException):
#     pass

# class BadRequest(CustomException):
#     pass

# class InvalidCredentials(CustomException):
#     pass

# class UnprocessableEntity(CustomException):
#     pass

# class DoesNotExist(CustomException):
#     pass

# class InternalServerError(DBException):
#     pass

# class NotFound(CustomException):
#     pass



