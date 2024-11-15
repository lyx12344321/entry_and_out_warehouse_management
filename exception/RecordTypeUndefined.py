class RecordTypeUndefined(Exception):
    """Raised when the record type is not defined"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)