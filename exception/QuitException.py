class QuitException(Exception):
    def __init__(self, message="正常退出"):
        self.message = message
        super().__init__(self.message)
    