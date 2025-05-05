
class NotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
        
class BadRequestException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
        
class InternalServerErrorException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
        
        