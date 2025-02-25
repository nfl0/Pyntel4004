"""Disassembly process supporting functions."""
# Import i4004 processor
from hardware.processor import Processor  # noqa

from typing import Tuple

# Shared imports
from shared.shared import get_opcodeinfobyopcode  # noqa


def disassemble_instruction(chip: Processor, _tps: list) -> \
        Tuple[str, str, int]:
    """
    Process a single instruction.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    _tps: list, mandatory
        List representing the memory of the i4004 into which the
        assembled instructions exist.

    Returns
    -------
    exe: str
        pre-formatted exe mnemonic ready for processing

    opcode: str
        Opcode of the current instruction

    words, int
        The number of words an instruction uses

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    opcode = _tps[chip.PROGRAM_COUNTER]
    oi = get_opcodeinfobyopcode(chip, opcode)
    words = (oi['words'])
    exe = get_opcodeinfobyopcode(chip, opcode)['mnemonic']
    return exe, opcode, words
