class EmptyException(Exception):
    def __init__(self, message="空输入"):
        self.message = message
        super().__init__(self.message)
    