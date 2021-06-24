class CustomError(Exception):
    """Exception raised for errors

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ElementNotFoundError(CustomError):
    pass


class WrongDateError(CustomError):
    pass


class NoExactTimeError(CustomError):
    pass


class NoBookingError(CustomError):
    pass


class DateUnavailableError(CustomError):
    pass


class DateOutOfBookingRangeError(CustomError):
    pass


class SlotsUnavailableError(CustomError):
    pass


class TicketsUnavailableError(CustomError):
    pass


class DateUnavailableError(CustomError):
    pass


class ProductNotFoundError(CustomError):
    pass
