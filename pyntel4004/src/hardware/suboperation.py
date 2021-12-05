"""Suboperations."""
from .exceptions import AddressOutOf8BitRange, \
    IncompatibleChunkBit, \
    InvalidBitValue, InvalidChunkValue, \
    InvalidCommandRegisterContent, InvalidCommandRegisterFormat, \
    InvalidPin10Value, InvalidRegister, \
    InvalidRegisterPair, NotABinaryNumber, \
    ProgramCounterOutOfBounds, ValueOutOfRangeForBits, \
    ValueTooLargeForAccumulator, \
    ValueTooLargeForRegister, ValueTooLargeForRegisterPair  # noqa

# Import typing library
from typing import Tuple


def rdx(self, character) -> int:
    """
    Read RAM status character X.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the Processor containing the registers, accumulator etc

    character:
        RAM STATUS CHARACTER to read

    Returns
    -------
    self.ACCUMULATOR
        The value read from the specified RAM STATUS CHARACTER

    """
    crb = self.read_current_ram_bank()
    chip, register, _none = \
        decode_command_register(self.COMMAND_REGISTER, 'DATA_RAM_STATUS_CHAR')
    self.ACCUMULATOR = self.STATUS_CHARACTERS[crb][chip][register][character]
    self.increment_pc(1)
    return self.ACCUMULATOR


def decode_command_register(command_register: str,
                            shape: str) -> Tuple[int, int, int]:
    """
    Convert the supplied CR into its component parts.

    Parameters
    ----------
    command_register : str, mandatory
        Content of the command register to convert

    shape:
        The shape/purpose of the command_register

    Returns
    -------
    chip: int
        The chip referred to

    register: int
        register

    address: int
        address referred to

    Raises
    ------
    InvalidCommandRegisterFormat

    """
    if shape not in ('DATA_RAM_CHAR', 'DATA_RAM_STATUS_CHAR',
                     'RAM_PORT', 'ROM_PORT'):
        raise InvalidCommandRegisterFormat('Shape: ' + shape)

    command_register = str(command_register)
    if shape == 'DATA_RAM_CHAR':
        if command_register == '0':
            raise InvalidCommandRegisterContent('Content: ' + command_register)
        chip = binary_to_decimal(command_register[:2])
        register = binary_to_decimal(command_register[2:4])
        address = binary_to_decimal(command_register[4:])

    if shape == 'DATA_RAM_STATUS_CHAR':
        if command_register == '0':
            raise InvalidCommandRegisterContent('Content: ' + command_register)
        chip = binary_to_decimal(command_register[:2])
        register = binary_to_decimal(command_register[2:4])
        address = '0'

    if shape == 'RAM_PORT':
        if command_register == '0':
            raise InvalidCommandRegisterContent('Content: ' + command_register)
        # Note that in this instance, "chip" refers to "port"
        chip = binary_to_decimal(command_register[:2])
        register = '0'
        address = '0'

    if shape == 'ROM_PORT':
        if command_register == '0':
            raise InvalidCommandRegisterContent('Content: ' + command_register)
        # Note that in this instance, "chip" refers to "port"
        chip = binary_to_decimal(command_register[:4])
        register = '0'
        address = '0'

    return int(chip), int(register), int(address)


def convert_to_absolute_address(self, rambank: int, chip: int,
                                register: int, address: int) -> int:
    """
    Convert a rambank, chip, register and address to an absolute RAM address.

    Parameters
    ----------
    self : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    rambank: integer, mandatory
        The currently selected RAM bank

    chip : integer, mandatory
        1 of 4 chips

    register : integer, mandatory
        1 of 4 registers

    address : integer, mandatory
        address within a page

    Returns
    -------
    absolute_address
        The address from 0 - 4095

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    absolute_address = (rambank * self.RAM_BANK_SIZE) + \
        (chip * self.RAM_CHIP_SIZE) + \
        (register * self.RAM_REGISTER_SIZE) + address
    return absolute_address


def split_address8(address: int) -> Tuple[str, str]:
    """
    Split a supplied decimal address into 2 4-bit words.

    Parameters
    ----------
    address: int, mandatory
        An 8-bit address in decimal format

    Returns
    -------
    address_left: str
        left-most 4 bits

    address_right: str
        right-most 4 bits

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    if (address < 0) or (address > 255):
        raise AddressOutOf8BitRange('Address: ' + str(address))

    address_left = bin(address)[2:].zfill(8)[:4]
    address_right = bin(address)[2:].zfill(8)[4:]
    return address_left, address_right


def increment_pc(self, words: int) -> int:
    """
    Increment the Program Counter by a specific number of words.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    words: int, mandatory
        The number of words to increment the Program Counter by

    Returns
    -------
    self.PROGRAM_COUNTER
        The new value of the Program Counter

    Raises
    ------
    ProgramCounterOutOfBounds

    Notes
    -----
    N/A

    """
    if self.PROGRAM_COUNTER + words > self.MEMORY_SIZE_RAM:
        raise ProgramCounterOutOfBounds('Program counter attempted to be' +
                                        ' set to ' +
                                        str(self.PROGRAM_COUNTER + words))
    self.PROGRAM_COUNTER = self.PROGRAM_COUNTER + words
    return self.PROGRAM_COUNTER


def inc_pc_by_page(self, pc: int) -> int:
    """
    Retrieve the pc's new value after being incremented by a page.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    pc: int, mandatory
        Current value of Program Counter

    Returns
    -------
    pc
        The new value of the Program Counter

    Raises
    ------
    ProgramCounterOutOfBounds

    Notes
    -----
    This function DOES NOT MODIFY the program counter, simply
    calculates the new  value of the counter. It is up to the
    calling  function to determine what to  do with the value.

    """
    if pc + self.PAGE_SIZE > self.MEMORY_SIZE_RAM:
        raise ProgramCounterOutOfBounds('Program counter attempted to be' +
                                        ' set to ' + str(pc + self.PAGE_SIZE))
    # Point the program counter to 1 page on
    pc = pc + self.PAGE_SIZE - 1
    return pc


def is_end_of_page(self, address: int, word: int) -> bool:
    """
    Determine if an instruction is located at the end of a memory page.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    address: int, mandatory
        Base address of the instruction

    word: int, mandatory
        Number of words in the instruction

    Returns
    -------
    True if the instruction is at the end of the memory page
    False if the instruction is not at the end of the memory page

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    page = address // self.PAGE_SIZE
    location = address - (page * self.PAGE_SIZE)
    word = word - 1
    return (location - word) == self.PAGE_SIZE - 1


def increment_register(self, register: int) -> int:
    """
    Increment the value in a register by 1.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    register: int, mandatory
        register to increment

    Returns
    -------
    self.REGISTERS[register]
        value of the register post increment

    Raises
    ------
    InvalidRegister

    Notes
    -----
    N/A

    """
    if register < 0 or register > (self.NO_REGISTERS - 1):
        raise InvalidRegister('Register: ' + str(register))

    self.REGISTERS[register] = self.REGISTERS[register] + 1
    if self.REGISTERS[register] > self.MAX_4_BITS:
        self.REGISTERS[register] = 0
    return self.REGISTERS[register]


def write_pin10(self, value: int) -> bool:
    """
    Write to pin 10 (reset pin).

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    value: int, mandatory
        value for pin 10

    Returns
    -------
    True
        if the value is set successfully

    Raises
    ------
    InvalidPin10Value

    Notes
    -----
    N/A

    """
    if value in (0, 1):
        self.PIN_10_SIGNAL_TEST = value
        return True
    raise InvalidPin10Value('PIN 10 attempted to be set to ' + str(value))


def write_ram_status(self, char: int) -> bool:
    """
    Write to a RAM status character.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    char: int, mandatory
        specified status character

    Returns
    -------
    True
        if the value is set successfully

    Raises
    ------
    N/A

    Notes
    -----
    No error checking is done in this function
    All parameters cannot be out of range, since the functions to
    place them in various registers etc all have range checking built in .

    Eventually - there will be error checking here

    """
    value = self.read_accumulator()
    crb = self.read_current_ram_bank()

    chip, register, _none = \
        decode_command_register(self.COMMAND_REGISTER,
                                'DATA_RAM_STATUS_CHAR')
    self.STATUS_CHARACTERS[crb][chip][register][char] = value
    return True


# Utility operations


def ones_complement(value: str, bits: int) -> str:
    """
    Converts a decimal into a one's compliment value of a specified bit length.

    Parameters
    ----------
    value: str: mandatory
        decimal value to convert

    bits: int, mandatory
        number of bits required for the conversion

    Returns
    -------
    The one's compliment binary value of the supplied decimal value.

    Raises
    ------
    InvalidBitValue: When a bit value of not 4, 8 or 12 is specified
    ValueOutOfRangeForBits: If the value supplied is either negative or is
                             out of range of the number of bits requested

    Notes
    -----
    N/A

    """
    if (bits not in [2, 4, 8, 12]):
        raise InvalidBitValue(' Bits: ' + str(bits))

    if (int(value) > ((2 ** bits) - 1)) or (int(value) < 0):
        raise ValueOutOfRangeForBits(' Value: ' + str(value) +
                                     ' Bits: ' + str(bits))

    # Perform a one's complement
    # i.e. invert all the bits

    binary = decimal_to_binary(bits, int(value))
    # binary = str(bin(value))[2:].zfill(bits)
    ones = ''
    for x in range(bits):
        if binary[x] == '1':
            ones = ones + '0'
        else:
            ones = ones + '1'
    return ones


def convert_decimal_to_n_bit_slices(bits: int, chunk: int,
                                    decimal: int, result: str = 'b') -> str:
    """
    Converts a decimal to several binary or decimal values of specific lengths.

    Parameters
    ----------
    bits: int, mandatory
        number of bits of the source data

    chunk: int, mandatory
        number of bits required per chunk

    decimal: int: mandatory
        decimal value to convert

    result: str: mandatory
        'd' will generate a decimal output
        'b' will generate a binary output

    Returns
    -------
    The binary value of the supplied decimal value.

    Raises
    ------
    IncompatibleChunkBit: When the chunks do not fit exactly within the bits
    InvalidBitValue: When a bit value of not 4, 8 or 12 is specified
    InvalidChunkValue: When a chunk value of not 4, 8 or 12 is specified
    ValueOutOfRangeForBits: If the value supplied is either negative or is
                             out of range of the number of bits requested

    Notes
    -----
    N/A

    """
    if (bits not in [2, 4, 8, 12]):
        raise InvalidBitValue(' Bits: ' + str(bits))

    if (chunk not in [2, 4, 8, 12]):
        raise InvalidChunkValue(' Chunk: ' + str(chunk))

    if bits % chunk != 0:
        raise IncompatibleChunkBit(' Bits: ' + str(bits) +
                                   ' Chunk: ' + str(chunk))

    if (decimal > ((2 ** bits) - 1)) or (decimal < 0):
        raise ValueOutOfRangeForBits(' Value: ' + str(decimal) +
                                     ' Bits: ' + str(bits))

    binary = decimal_to_binary(bits, decimal)
    chunks = [binary[i:i+chunk] for i in range(0, len(binary), chunk)]
    if result != 'b':
        decimals = []
        for element in chunks:
            decimals.append(binary_to_decimal(element))
        chunks = decimals
    return chunks


def decimal_to_binary(bits: int, decimal: int) -> str:
    """
    Converts a decimal value into a binary value of a specified bit length.

    Parameters
    ----------
    bits: int, mandatory
        number of bits required for the conversion

    decimal: int: mandatory
        decimal value to convert

    Returns
    -------
    The binary value of the supplied decimal value.

    Raises
    ------
    InvalidBitValue: When a bit value of not 4, 8 or 12 is specified
    ValueOutOfRangeForBits: If the value supplied is either negative or is
                             out of range of the number of bits requested

    Notes
    -----
    N/A

    """
    if (bits not in [2, 4, 8, 12]):
        raise InvalidBitValue(' Bits: ' + str(bits))

    if (decimal > ((2 ** bits) - 1)) or (decimal < 0):
        raise ValueOutOfRangeForBits(' Value: ' + str(decimal) +
                                     ' Bits: ' + str(bits))

    # Convert decimal to binary
    binary = bin(decimal)[2:].zfill(bits)
    return binary


def binary_to_decimal(binary: str) -> int:
    """
    Converts a string value(which must be in binary form) to a decimal value.

    Parameters
    ----------
    binary: str, mandatory
        a string which represents the binary value

    Returns
    -------
    The decimal value of the supplied binary value

    Raises
    ------
    NotABinaryNumber: When a non-binary number is supplied

    Notes
    -----
    N/A

    """
    if len(binary) == 0:
        binary = '<empty>'
        raise NotABinaryNumber('"' + binary + '"')

    if len(binary.replace('0', '').replace('1', '')) != 0:
        raise NotABinaryNumber('"' + binary + '"')

    # Convert binary to decimal
    return int(binary, 2)


def flip_wpm_counter(self) -> str:
    """
    Flip the WPM counter.

    Two WPM instructions must always appear in close succession; that is,
    each time one WPM instruction references a half byte of program RAM
    as indicated by an SRC address, another WPM must access the other half
    byte before the SRC address is altered.
    This internal counter keeps track of which half-byte is being accessed.
    If only one WPM occurs, this counter will be out of sync with the
    program and errors will occur.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    self.WPM_COUNTER
        The flipped value of the WPM counter(either "LEFT" or "RIGHT")

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    if self.WPM_COUNTER == 'LEFT':
        self.WPM_COUNTER = 'RIGHT'
    else:
        self.WPM_COUNTER = 'LEFT'
    return self.WPM_COUNTER


def check_overflow(self) -> Tuple[int, int]:
    """
    Check if an overflow is detected.

    If the result is more than a 4-bit number(MAX_4_BITS),
    then an overflow is detected.

    If there is an overflow detected, set the carry bit,
    otherwise reset the carry bit.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    self.ACCUMULATOR
        The value of the accumulator after adjusting for overflow
    self.CARRY
        The carry bit

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    if self.ACCUMULATOR > self.MAX_4_BITS:
        self.ACCUMULATOR = self.ACCUMULATOR - self.MAX_4_BITS + 1
        self.set_carry()
    else:
        self.reset_carry()
    return self.ACCUMULATOR, self.CARRY


def set_accumulator(self, value: int) -> int:
    """
    Insert a value into the Accumulator.

    Parameters
    ----------
    self: Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    value: int, mandatory
        The value to insert

    Returns
    -------
    value
        The value of the accumulator

    Raises
    ------
    ValueTooLargeForAccumulator

    Notes
    -----
    N/A

    """
    if value > self.MAX_4_BITS:
        raise ValueTooLargeForAccumulator(' Value: ' + str(value))
    self.ACCUMULATOR = value
    return value
