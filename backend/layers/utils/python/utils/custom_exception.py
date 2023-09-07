

class CustomException(Exception):
    def __init__(self, status_code, message,  error_code=None, save_error=False):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.save_error = save_error
        super().__init__(message)
