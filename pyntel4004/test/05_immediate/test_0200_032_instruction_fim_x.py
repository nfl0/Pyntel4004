# Using pytest
# Test the fim instructions of an instance of an i4004(processor)

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

import pickle  # noqa
import pytest  # noqa
import random  # noqa

from hardware.processor import Processor  # noqa
from hardware.suboperations.utility import decimal_to_binary  # noqa
from hardware.suboperations.registers import insert_register  # noqa


@pytest.mark.parametrize("registerpair", [0, 1, 2, 3, 4, 5, 6, 7])
def test_validate_instruction(registerpair):
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[32 + (registerpair * 2)]
    known = {"opcode": 32 + (registerpair * 2), "mnemonic": "fim(" + str(registerpair) + "p,data8)", "exe": 21.6, "bits": ["0010", decimal_to_binary(4, (2 * registerpair)), 'xxxx', 'xxxx'], "words": 2}  # noqa
    assert op == known


@pytest.mark.parametrize("registerpair", [0, 1, 2, 3, 4, 5, 6, 7])
def test_scenario1(registerpair):
    """Test FIM instruction functionality."""
    chip_test = Processor()
    chip_base = Processor()

    rv = random.randint(0, 205)  # Select a random 4-bit value

    # Perform the instruction under test:
    chip_test.PROGRAM_COUNTER = 0

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 0
    chip_base.increment_pc(2)
    # Convert a register pair into a base register for insertion
    base_register = registerpair * 2
    chip_base.insert_register(base_register, (rv >> 4) & 15)   # Bit-shift right and remove low bits   # noqa
    chip_base.insert_register(base_register + 1, rv & 15)      # Remove low bits                       # noqa

    # Carry out the instruction under test
    # Perform an FIM operation
    Processor.fim(chip_test, registerpair, rv)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()
    assert chip_test.REGISTERS[base_register] == chip_base.REGISTERS[base_register]  # noqa
    assert chip_test.REGISTERS[base_register + 1] == chip_base.REGISTERS[base_register + 1]  # noqa

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
