# Using pytest
# Test the INC instructions of an instance of an i4004(processor)

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

import pickle  # noqa
import pytest  # noqa


from hardware.processor import Processor  # noqa
from hardware.suboperations.utility import decimal_to_binary  # noqa
from hardware.suboperations.registers import insert_register  # noqa


@pytest.mark.parametrize("register", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])  # noqa
def test_validate_instruction(register):
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[96 + register]
    known = {"opcode": 96 + register, "mnemonic": "inc(" + str(register) + ")", "exe": 10.8, "bits": ["0110", decimal_to_binary(4, register)], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("register", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])  # noqa
def test_scenario1(register):
    """Test INC instruction functionality."""
    chip_test = Processor()
    chip_base = Processor()

    # Perform the instruction under test:
    # 3 increments of register "register"
    Processor.inc(chip_test, register)
    Processor.inc(chip_test, register)
    Processor.inc(chip_test, register)

    # Simulate conditions at end of instruction in base chip
    chip_base.increment_pc(3)
    insert_register(chip_base, register, 3)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_register(0) == chip_base.read_register(0)

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


def test_scenario2():
    """Test INC instruction functionality (scenario 2)."""
    chip_test = Processor()
    chip_base = Processor()

    # Perform the instruction under test:
    # Use register 0 to attempt to raise an exception
    for _ in range(14):
        Processor.inc(chip_test, 0)

    # Simulate conditions at end of instruction in base chip
    chip_base.increment_pc(14)
    insert_register(chip_test, 0, 0)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_register(0) == chip_base.read_register(0)

    # Pickling each chip and comparing will show complete equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
