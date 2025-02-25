# Using pytest
# Test the initialisation of an instance of an i4004(processor)

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

import pickle  # noqa

from hardware.processor import Processor            # noqa


def test_validate_instruction():
    """Ensure instruction's characteristics are valid."""
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[0]
    known = {'opcode': 0, 'mnemonic': 'nop()', 'exe': 10.8, 'bits': ['0000', '0000'], 'words': 1}  # noqa
    assert known == op


def test_post_nop_chip():
    """Test NOP instruction."""
    # Perform the instruction under test:
    Processor.nop(chip_test)

    # Simulate conditions at end of instruction in base chip
    chip_base.increment_pc(1)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.
    assert chip_test.read_program_counter() == chip_base.read_program_counter()

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


chip_base = Processor()
chip_test = Processor()
