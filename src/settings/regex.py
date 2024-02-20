class Regex:
    
    USERNAME = "^(?=.*[a-zA-Z0-9])(?!^\d+$)[a-zA-Z0-9]+$"
    PASSWORD = '^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[a-zA-Z\d!@#$%^&*(),.?":{}|<>]{8,}$'
    NAME = "^[a-zA-Z ]+$"
    PHONE = "^[0-9]{10}$"
    PRICE = "^\d+$"
    TICKETS = "^\d+$"
    