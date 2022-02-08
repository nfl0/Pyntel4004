"""Disssembler main module."""

# Import System modules
import os
import sys
sys.path.insert(1, '..' + os.sep + 'src')

# Import i4004 processor
from hardware.processor import Processor  # noqa

# Import supporting functions
from disassembler.dis_supporting import disassemble_instruction  # noqa
# Shared imports
from shared.shared import retrieve_program, translate_mnemonic  # noqa


###############################################################################################  # noqa
#  _ _  _    ___   ___  _  _     _____  _                                  _     _            #  # noqa
# (_) || |  / _ \ / _ \| || |   |  __ \(_)                                | |   | |           #  # noqa
#  _| || |_| | | | | | | || |_  | |  | |_ ___  __ _ ___ ___  ___ _ __ ___ | |__ | | ___ _ __  #  # noqa
# | |__   _| | | | | | |__   _| | |  | | / __|/ _` / __/ __|/ _ \ '_ ` _ \| '_ \| |/ _ \ '__| #  # noqa
# | |  | | | |_| | |_| |  | |   | |__| | \__ \ (_| \__ \__ \  __/ | | | | | |_) | |  __/ |    #  # noqa
# |_|  |_|  \___/ \___/   |_|   |_____/|_|___/\__,_|___/___/\___|_| |_| |_|_.__/|_|\___|_|    #  # noqa
#                                                                                             #  # noqa                                                                         #
###############################################################################################  # noqa


def disassemble(chip: Processor, location: str, pc: int) -> bool:
    """
    Control the dissassembly of a previously assembled program.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    location : str, mandatory
        The location to which the program should be loaded

    pc : int, mandatory
        The program counter value to commence execution

    Returns
    -------
    True        in all instances

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """

    chip.PROGRAM_COUNTER = pc
    opcode = 0
    _tps = retrieve_program(chip, location)
    # pseudo-opcode (directive) for "end"
    while (opcode != 256) or \
            (chip.PROGRAM_COUNTER <= chip.MEMORY_SIZE_PRAM - 1):
        if chip.PROGRAM_COUNTER == chip.MEMORY_SIZE_PRAM:
            return True
        if opcode == 256:
            return True
        exe, opcode, words = disassemble_instruction(chip, _tps)
        # Translate and print instruction
        translate_mnemonic(chip, _tps, exe, opcode, 'D', words)
    return True
