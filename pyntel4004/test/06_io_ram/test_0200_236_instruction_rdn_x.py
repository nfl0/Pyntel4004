# Using pytest
# Test the RDn instructions of an instance of an i4004(processor)

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')
sys.path.insert(2, '..' + os.sep + 'test')

import pickle  # noqa
import pytest  # noqa

from hardware.processor import Processor  # noqa
from utils import encode_command_register  # noqa


def test_validate_rdn_instruction():
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    # There are 4 rdN instructions.
    op = chip_test.INSTRUCTIONS[236]
    known = {"opcode": 236, "mnemonic": "rd0()", "exe": 10.8, "bits": ["1110", '1100'], "words": 1}  # noqa
    assert op == known

    op = chip_test.INSTRUCTIONS[237]
    known = {"opcode": 237, "mnemonic": "rd1()", "exe": 10.8, "bits": ["1110", '1101'], "words": 1}  # noqa
    assert op == known

    op = chip_test.INSTRUCTIONS[238]
    known = {"opcode": 238, "mnemonic": "rd2()", "exe": 10.8, "bits": ["1110", '1110'], "words": 1}  # noqa
    assert op == known

    op = chip_test.INSTRUCTIONS[239]
    known = {"opcode": 239, "mnemonic": "rd3()", "exe": 10.8, "bits": ["1110", '1111'], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("rambank", [0, 1, 2, 3])
@pytest.mark.parametrize("chip", [0, 1, 2, 3])
@pytest.mark.parametrize("register", [0, 1, 2, 3])
@pytest.mark.parametrize("char", [0, 1, 2, 3])
def test_rdn_scenario1(rambank, chip, register, char):
    """Test instruction RDn"""
    from random import randint

    chip_test = Processor()
    chip_base = Processor()

    value = randint(0, 15)

    address = encode_command_register(chip, register, 0,
                                      'DATA_RAM_STATUS_CHAR')
    chip_test.CURRENT_RAM_BANK = rambank
    chip_test.COMMAND_REGISTER = address
    chip_test.STATUS_CHARACTERS[rambank][chip][register][char] = value

    # Perform the instruction under test:
    if char == 0:
        Processor.rd0(chip_test)
    if char == 1:
        Processor.rd1(chip_test)
    if char == 2:
        Processor.rd2(chip_test)
    if char == 3:
        Processor.rd3(chip_test)

    # Simulate conditions at end of instruction in base chip
    chip_base.COMMAND_REGISTER = address
    chip_base.CURRENT_RAM_BANK = rambank
    chip_base.increment_pc(1)
    chip_base.set_accumulator(value)
    chip_base.STATUS_CHARACTERS[rambank][chip][register][char] = value

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    assert chip_test.read_program_counter() == chip_base.read_program_counter()
    assert chip_test.read_accumulator() == chip_base.read_accumulator()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
