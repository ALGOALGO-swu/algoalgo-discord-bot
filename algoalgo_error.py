class UserDefinedException(Exception):
    message = "Undefined Error"
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message
