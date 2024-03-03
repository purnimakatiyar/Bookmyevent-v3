from marshmallow import Schema, fields, validate
from settings.regex import Regex


class AuthSchema(Schema):
    username = fields.Str(required = True, validate=validate.Regexp(Regex.USERNAME))
    password = fields.Str(required = True, validate=validate.Regexp(Regex.PASSWORD))
    
    
class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Regexp(Regex.USERNAME))
    password = fields.Str(required = True, validate=validate.Regexp(Regex.PASSWORD))
    name = fields.Str(required = True, validate=validate.Regexp(Regex.NAME))
    phone = fields.Str(required = True, validate=validate.Regexp(Regex.PHONE))
    
    
class UpdateUserSchema(Schema):
    password = fields.Str(validate=validate.Regexp(Regex.PASSWORD), missing=None)
    name = fields.Str(validate=validate.Regexp(Regex.NAME), missing=None)
    phone = fields.Str(validate=validate.Regexp(Regex.PHONE), missing=None)
    
    
class EventSchema(Schema):
    event_name = fields.Str(required = True, validate=validate.Regexp(Regex.NAME))
    event_date = fields.Str(required = True)
    location = fields.Str(required = True)
    price = fields.Str(required = True, validate=validate.Regexp(Regex.PRICE))
    category = fields.Str(required = True)
    ticket_qty = fields.Str(required = True, validate=validate.Regexp(Regex.TICKETS))
    
class UpdateEventSchema(Schema):
    event_name = fields.Str(validate=validate.Regexp(Regex.NAME), missing=None)
    event_date = fields.Str(missing=None)
    location = fields.Str(missing=None)
    price = fields.Str(validate=validate.Regexp(Regex.PRICE), missing=None)
    category = fields.Str(missing=None)
    ticket_qty = fields.Str(validate=validate.Regexp(Regex.TICKETS), missing=None)
    
class BookEventSchema(Schema):
    ticket_qty = fields.Str(required=True)
    
class ViewEventSchema(Schema):
    event_name = fields.Str(dump_only = True)
    event_date = fields.Str(dump_only= True)
    location = fields.Str(dump_only= True)
    price = fields.Str(dump_only= True)
    category = fields.Str(dump_only= True)
    ticket_qty = fields.Str(dump_only= True)
    
    
class ViewUserSchema(Schema):
    username = fields.Str(dump_only= True)
    name = fields.Str(dump_only= True)
    phone = fields.Str(dump_only= True)
    

    