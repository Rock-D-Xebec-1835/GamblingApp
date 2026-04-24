class ValidationException(Exception):
    def __init__(self, message, error_type=None, field=None, value=None):
        super().__init__(message)
        self.error_type = error_type
        self.field = field
        self.value = value

class StakeValidationException(ValidationException):
    pass

class BetValidationException(ValidationException):
    pass

class LimitValidationException(ValidationException):
    pass

class ProbabilityValidationException(ValidationException):
    pass
