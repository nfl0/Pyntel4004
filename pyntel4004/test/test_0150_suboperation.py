# Using pytest
# Test the suboperations of an instance of an i4004(processor)

import sys
import pickle

import pytest

sys.path.insert(1, '../src')

import hardware.suboperation # noqa
from hardware.processor import processor  # noqa
from hardware.exceptions import ValueTooLargeForRegister, \
        ValueTooLargeForRegisterPair, InvalidRegister, \
        InvalidRegisterPair, ProgramCounterOutOfBounds # noqa


##############################################################################
#                      Set/Reset Carry Flag                                  #
##############################################################################
def test_suboperation_set_carry():
    chip_base = processor()
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    chip_base.CARRY = 1

    # Perform the operation under test:
    # setting carry
    processor.set_carry(chip_test)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert (chip_test.read_carry() == chip_base.read_carry())

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


def test_suboperation_reset_carry():
    chip_base = processor()
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    chip_base.CARRY = 0

    # Perform the operation under test:
    # resetting carry
    processor.reset_carry(chip_test)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert (chip_test.read_carry() == chip_base.read_carry())

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


##############################################################################
#                      Read Complement of Carry Flag                         #
##############################################################################
@pytest.mark.parametrize("carry", [0, 1])
def test_suboperation_read_complement_carry(carry):
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    chip_test.CARRY = carry
    complement_carry = 1 if carry == 0 else 0

    # Perform the operation under test:
    # N/A

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    # Also ensure the carry flag is still correctly set
    assert (chip_test.read_complement_carry() == complement_carry)
    assert (chip_test.read_carry() == chip_test.CARRY)

    # Pickling each chip and comparing will show equality or not.
    # N/A

##############################################################################
#                      Insert Register                                       #
##############################################################################
@pytest.mark.parametrize("register", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])  # noqa
def test_suboperation_insert_register_scenario1(register):
    chip_base = processor()
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    chip_base.REGISTERS[register] = 5

    # Perform the operation under test:
    # insert a value of 5 into each register
    processor.insert_register(chip_test, register, 5)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert (chip_test.read_program_counter() == chip_base.read_program_counter())

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


def test_suboperation_insert_register_scenario2():
    chip_base = processor()
    chip_test = processor()

    # Perform the operation under test:
    # attempting to insert a value larger than the register can hold
    with pytest.raises(Exception) as e:
        assert (processor.insert_register(chip_test, 3, 25))
    assert (str(e.value) == "Register: 3,Value: 25")
    assert (e.type == ValueTooLargeForRegister)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert(chip_test.read_register(3) == 0)

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


def test_suboperation_insert_register_scenario3():
    chip_base = processor()
    chip_test = processor()

    # Perform the operation under test:
    # attempting to insert a value into an invalid register
    with pytest.raises(Exception) as e:
        assert (processor.insert_register(chip_test, 25, 3))
    assert (str(e.value) == "Register: 25")
    assert (e.type == InvalidRegister)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.

    # N/A - the operation will completely fail - the chip will be as it was
    # in the base state

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))

##############################################################################
#                      Read Register                                         #
##############################################################################
@pytest.mark.parametrize("register", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])  # noqa
def test_suboperation_read_register(register):
    chip_test = processor()

    # Perform the operation under test:
    # insert a value of 5 into each register
    chip_test.REGISTERS[register] = 5

    # Simulate conditions at end of operation in base chip
    # N/A

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert (chip_test.read_register(register) == 5)


##############################################################################
#                      Insert Register Pair                                  #
##############################################################################
@pytest.mark.parametrize("registerpair", [0, 1, 2, 3, 4, 5, 6, 7])  # noqa
def test_suboperation_insert_registerpair_scenario1(registerpair):
    chip_base = processor()
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    chip_base.REGISTERS[registerpair * 2] = 15
    chip_base.REGISTERS[(registerpair * 2) + 1] = 14  # Perform the operation under test:

    # insert a value of 254 into a registerpair
    processor.insert_registerpair(chip_test, registerpair, 254)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert (chip_test.read_program_counter() == chip_base.read_program_counter())

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


def test_suboperation_insert_registerpair_scenario2():
    chip_base = processor()
    chip_test = processor()

    # Perform the operation under test:
    # attempting to insert a value larger than the register pair can hold
    with pytest.raises(Exception) as e:
        assert (processor.insert_registerpair(chip_test, 3, 300))
    assert (str(e.value) == "Register Pair: 3,Value: 300")
    assert (e.type == ValueTooLargeForRegisterPair)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert(chip_test.read_register(3) == 0)

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


def test_suboperation_insert_registerpair_scenario3():
    chip_base = processor()
    chip_test = processor()

    # Perform the operation under test:
    # attempting to insert a value into an invalid registerpair
    with pytest.raises(Exception) as e:
        assert (processor.insert_registerpair(chip_test, 9, 3))
    assert (str(e.value) == "Register Pair: 9")
    assert (e.type == InvalidRegisterPair)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.

    # N/A - the operation will completely fail - the chip will be as it was
    # in the base state

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


##############################################################################
#                      Read Register Pair                                    #
##############################################################################
def test_suboperation_read_registerpair():
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    chip_test.REGISTERS[6] = 15
    chip_test.REGISTERS[7] = 14

    # Perform the operation under test:
    # Read a value from register pair 3 (registers 6 and 7)
    assert (chip_test.read_registerpair(3) == 254)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    # N/A


##############################################################################
#                      Increment Program Counter                             #
##############################################################################
@pytest.mark.parametrize("words", [0, 1, 2])  # noqa
def test_suboperation_increment_pc_scenario1(words):
    chip_base = processor()
    chip_test = processor()

    # Simulate conditions at end of operation in base chip
    chip_base.PROGRAM_COUNTER = chip_test.MEMORY_SIZE_RAM - 10 + words

    # Simulate conditions at end of operation in base chip
    chip_test.PROGRAM_COUNTER = chip_test.MEMORY_SIZE_RAM - 10

    # Increment the Program Counter by 0, then 1, then 2 words
    processor.increment_pc(chip_test, words)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.
    assert (chip_test.read_program_counter() == chip_base.read_program_counter())

    # Pickling each chip and comparing will show equality or not.
    assert (pickle.dumps(chip_test) == pickle.dumps(chip_base))


def test_suboperation_increment_pc_scenario3():
    chip_base = processor()
    chip_test = processor()

    chip_test.PROGRAM_COUNTER = chip_test.MEMORY_SIZE_RAM - 1
    chip_base.PROGRAM_COUNTER = chip_test.PROGRAM_COUNTER

    # Perform the operation under test:
    # attempting to increment the Program Counter beyond the end of memory
    with pytest.raises(Exception) as e:
        assert (processor.increment_pc(chip_test, 2))
    assert (str(e.value) == "Program counter attempted to be set to 4097")
    assert (e.type == ProgramCounterOutOfBounds)

    # Make assertions that the base chip is now at the same state as
    # the test chip which has been operated on by the operation under test.

    assert (chip_test.read_program_counter() == chip_base.read_program_counter())
