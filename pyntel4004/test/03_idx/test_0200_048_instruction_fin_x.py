# Using pytest
# Test the FIN instructions of an instance of an i4004(processor)

# Import system modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

import pickle  # noqa
import pytest  # noqa


from hardware.processor import Processor  # noqa
from hardware.suboperations.utility import convert_decimal_to_n_bit_slices, \
     decimal_to_binary  # noqa
from hardware.suboperations.registers import insert_register   # noqa


@pytest.mark.parametrize("registerpair", [0, 1, 2, 3, 4, 5, 6, 7])
def test_validate_instruction(registerpair):
    """Ensure instruction's characteristics are valid."""
    chip_test = Processor()
    # Validate the instruction's opcode and characteristics:
    op = chip_test.INSTRUCTIONS[48 + (registerpair * 2)]
    known = {"opcode": 48 + (registerpair * 2), "mnemonic": "fin(" + str(registerpair) + ")", "exe": 21.6, "bits": ["0011", decimal_to_binary(4, registerpair * 2)], "words": 1}  # noqa
    assert op == known


@pytest.mark.parametrize("values", [[1, 123, 23], [1, 234, 34],
                                    [2, 12, 5], [3, 100, 90], [4, 0, 12],
                                    [5, 44, 100], [6, 15, 48], [7, 255, 0]])
def test_scenario1(values):
    """Test FIN instruction functionality."""
    chip_test = Processor()
    chip_base = Processor()

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 256
    chip_base.RAM[values[2]] = values[1]
    registervalue = convert_decimal_to_n_bit_slices(8, 4, values[1], 'd')  # noqa
    chip_base.REGISTERS[0] = registervalue[0]
    chip_base.REGISTERS[1] = registervalue[1]

    chip_test.PROGRAM_COUNTER = 255
    chip_test.RAM[values[2]] = values[1]
    chip_test.REGISTERS[0] = registervalue[0]
    chip_test.REGISTERS[1] = registervalue[1]

    # Perform the instruction under test:
    # Fetch indirect from..... (command at end of page)
    left, right = Processor.fin(chip_test, values[0])

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    left_r = chip_test.read_register(values[0])
    right_r = chip_test.read_register(values[0]+1)

    assert left == left_r
    assert right == right_r
    assert chip_test.PROGRAM_COUNTER == 256

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)


@pytest.mark.parametrize("values", [[1, 123, 23], [1, 234, 34],
                                    [2, 12, 5], [3, 100, 90], [4, 0, 12],
                                    [5, 44, 100], [6, 15, 48], [7, 255, 0]])
def test_scenario2(values):
    """Test DCL instruction functionality (scenario 2)."""
    chip_test = Processor()
    chip_base = Processor()

    # Simulate conditions at end of instruction in base chip
    chip_base.PROGRAM_COUNTER = 11
    chip_base.RAM[values[2]] = values[1]
    registervalue = convert_decimal_to_n_bit_slices(8, 4, values[1], 'd')  # noqa
    chip_base.REGISTERS[0] = registervalue[0]
    chip_base.REGISTERS[1] = registervalue[1]

    chip_test.PROGRAM_COUNTER = 10
    chip_test.RAM[values[2]] = values[1]
    chip_test.REGISTERS[0] = registervalue[0]
    chip_test.REGISTERS[1] = registervalue[1]

    # Perform the instruction under test:
    # Fetch indirect from
    left, right = Processor.fin(chip_test, values[0])

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the instruction under test.

    left_r = chip_test.read_register(values[0])
    right_r = chip_test.read_register(values[0]+1)

    assert left == left_r
    assert right == right_r
    assert chip_test.PROGRAM_COUNTER == 11

    # Pickling each chip and comparing will show equality or not.
    assert pickle.dumps(chip_test) == pickle.dumps(chip_base)
