class ValueTooLargeForRegister(Exception):
    """Raised when the value for a register is too large"""
    pass


class InvalidEndOfPage(Exception):
    """Raised when it is impossible to determine the end of a page """
    pass


class ProgramCounterOutOfBounds(Exception):
    """Raised when the program counter is forced beyond the end of memory """
    pass


class InvalidPin10Value(Exception):
    """Raised when the value of PIN 10 is attempted to be set to NOT 0 or 1 """
    pass


class InvalidRamBank(Exception):
    """Raised when the attempting to select a RAM bank > 7 """
    pass


class NotABinaryNumber(Exception):
    """Raised when a supplied binary number is NOT binary """
    pass


class InvalidRegister(Exception):
    """Raised when an invalid register is supplied """
    pass


class InvalidRegisterPair(Exception):
    """Raised when an invalid register pair is supplied """
    pass


class ValueTooLargeForRegisterPair(Exception):
    """Raised when the value for a register pair is too large"""
    pass


class ValueTooLargeForAccumulator(Exception):
    """Raised when the value for the Accumulator is too large"""
    pass

