class IncorrectMove(Exception):
    def __init__(self, message):
        super().__init__(message)


class ParseError(Exception):
    def __init__(self, message):
        super().__init__(message)
