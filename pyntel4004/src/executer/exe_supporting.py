"""Assembly process supporting functions."""

import json
from typing import Tuple

from hardware.processor import Processor
from shared.shared import determine_filetype


def load_bin(inputfile: str, chip: Processor, quiet: bool) -> str:
    """
    Reload an already assembled binary program.

    Parameters
    ----------
    inputfile: str, mandatory
        filename of a .bin file

    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    quiet: bool, mandatory
        If output should be output or not

    Returns
    -------
    memory_space: str
        rom or ram (depending on the target memory space)

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    if not quiet:
        print(' Filetype: Binary assembled machine code\n')
    location = 0
    memory_space = 'ram'
    programbytearray = bytearray()
    try:
        with open(inputfile, "rb") as f:
            byte = f.read(1)
            while byte:
                programbytearray += byte
                byte = f.read(1)
                location = location + 1

    except IOError:
        print('Error While Opening the file!')

    # Place program in memory
    location = 0
    memory_space = 'ram'

    for i in programbytearray:
        chip.PRAM[location] = i
        location = location + 1

    return memory_space


def load_obj(inputfile: str, chip: Processor, quiet: bool) -> Tuple[str, list]:
    """
    Reload an already assembled object program.

    Parameters
    ----------
    inputfile: str, mandatory
        filename of an .obj file

    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    quiet: bool, mandatory
        If output should be output or not

    Returns
    -------
    memory_space: str
        rom or ram (depending on the target memory space)

    labels: list
        list of labels contained within the program's object module

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """

    if not quiet:
        print(' Filetype: Object module with label tables etc.\n')
    with open(inputfile, "r", encoding='utf-8') as programfile:
        data = json.load(programfile)

    # Get data for memory load
    memory_space = data['location']

    # Get labels
    labels = data['labels']

    # Place program in memory
    location = 0

    for i in data['memory']:
        if memory_space == 'rom':
            chip.ROM[location] = int(i, 16)
        else:
            chip.PRAM[location] = int(i, 16)
        location = location + 1
    return memory_space, labels


def reload(inputfile: str, chip: Processor,
           quiet: bool) -> Tuple[str, int, list]:
    """
    Reload an already assembled program and execute it.

    Parameters
    ----------
    inputfile: str, mandatory
        filename of a .obj or a .bin file

    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    quiet: bool, mandatory
        If output should be output or not
    Returns
    -------
    memory_space: str
        rom or ram (depending on the target memory space)

    pc:  int
        location to commence execution of the assembled program

    labels: list
        list of labels from object module only

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """

    filetype = determine_filetype(inputfile)

    # Blank list of labels
    labels = []

    if filetype == 'OBJ':
        memory_space, labels = load_obj(inputfile, chip, quiet)

    if filetype == 'BIN':
        memory_space = load_bin(inputfile, chip, quiet)

    # Always return zero as a program counter
    return memory_space, 0, labels


def set_prompts(req: str) -> Tuple[str, str, str, bool]:
    """

    Ensure prompts for the monitor are set correctly

    Parameters
    ----------
    req : str, mandatory
        The state that the monitor is in (drives the prompts)

    Returns
    -------
    classic_prompt: str
        "Normal" prompt

    breakout_prompt: str
        Prompt to use when the system is in breakpoint mode

    prompt: str
        Current prompt to use

    result : bool
        Always <None>

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    classic_prompt = '>>> '
    breakout_prompt = 'B>> '
    if req == 'INITIAL':
        prompt = classic_prompt

    if req == 'BREAKOUT':
        prompt = breakout_prompt
    return classic_prompt, breakout_prompt, prompt, None


def is_breakpoint(breakpoints: list, pc: int) -> bool:
    """
    Determine if the current programme counter is at a breakpoint.

    Parameters
    ----------
    breakpoints : list, mandatory
        A list of the predetermined breakpoints

    pc: int, mandatory
        The current value of the program counter

    Returns
    -------
    True        if the current program counter is at a breakpoint
    False       if the current program counter is not at a breakpoint

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    for i in breakpoints:
        if str(i) == str(pc):
            return True
    return False


def print_stack(chip: Processor) -> None:
    """
    Print the stack values (along with the pointer).

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    Returns
    -------
    N/A

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    for _i in range(chip.STACK_SIZE-1, -1, -1):
        if _i == chip.STACK_POINTER:
            pointer = '==>'
        else:
            pointer = '-->'
        print("[ " + str(_i) + "] " + pointer + "[ " +
              str(chip.STACK[_i]) + ' ]')


def process_simple_monitor_command(chip: Processor, monitor_command: str,
                                   monitor: bool, opcode: str) \
        -> Tuple[bool, bool, str, str]:
    """
    Take appropriate action depending on the command supplied.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    monitor_command: str, mandatory
        Command given by the user.

    monitor: bool, mandatory
        Whether or not the monitor is currently "on" or "off"

    opcode: str, mandatory
        Opcode of the current instruction

    Returns
    -------
    True/False: bool  if the code should continue with monitor on or off
    None              if the monitor should be disabled

    monitor: bool
        Whether or not the monitor is currently "on" or "off"

    monitor_command: str
        The command that was entered by the user

    opcode: str
        Opcode of the current instruction

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    if monitor_command == 'stack':
        print_stack(chip)
    elif monitor_command == 'pc':
        print('PC = ', chip.PROGRAM_COUNTER)
    elif monitor_command == 'carry':
        print('CARRY = ', chip.read_carry())
    elif monitor_command == 'ram':
        print('RAM = ', chip.RAM)
    elif monitor_command == 'pram':
        print('PRAM = ', chip.PRAM)
    elif monitor_command == 'rom':
        print('ROM = ', chip.ROM)
    elif monitor_command == 'acc':
        print('ACC =', chip.read_accumulator())
    elif monitor_command == 'pin10':
        print('PIN10 = ', chip.read_pin10())
    elif monitor_command == 'crb':
        print('CURRENT RAM BANK = ', chip.read_current_ram_bank())
    return True, monitor, monitor_command, opcode


def deal_with_monitor_command(chip: Processor, monitor_command: str,
                              breakpoints, monitor: bool, opcode: str) \
        -> Tuple[bool, bool, str, str, str]:
    """
    Take appropriate action depending on the command supplied.

    Parameters
    ----------
    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    monitor_command: str, mandatory
        Command given by the user.

    breakpoints : list, mandatory
        A list of the predetermined breakpoints

    monitor: bool, mandatory
        Whether or not the monitor is currently "on" or "off"

    opcode: str, mandatory
        Opcode of the current instruction

    Returns
    -------
    True/False: bool  if the code should continue with monitor on or off
    None              if the monitor should be disabled

    monitor: bool
        Whether or not the monitor is currently "on" or "off"

    monitor_command: str
        The command that was entered by the user

    opcode: str,
        Opcode of the current instruction

    prompt: str,
        Style of prompt to continue using (breakpoint or initial)

    Raises
    ------
    N/A

    Notes
    -----
    Function will return a value of -1 if the monitor command is invalid.

    """
#   mccabe: MC0001 / deal_with_monitor_command is too complex (18) - start
#   mccabe: MC0001 / deal_with_monitor_command is too complex (16)
#   mccabe: MC0001 / deal_with_monitor_command is too complex (5)

    classic_prompt, breakout_prompt, prompt, _ = set_prompts('INITIAL')
    if monitor_command == '':
        return True, monitor, monitor_command, opcode, breakout_prompt
    if monitor_command == 'regs':
        print('0-> ' + str(chip.REGISTERS) + ' <-15')
        return True, monitor, monitor_command, opcode, breakout_prompt
    if monitor_command in (['stack', 'pc', 'carry', 'ram', 'pram',
                            'rom', 'acc', 'pin10', 'crb']):
        result, monitor, monitor_command, opcode = \
            process_simple_monitor_command(chip, monitor_command,
                                           monitor, opcode)
        if result is False:
            fprompt = classic_prompt
        else:
            fprompt = breakout_prompt
        return result, monitor, monitor_command, opcode, fprompt
    if monitor_command[:3] == 'reg':
        register = int(monitor_command[3:])
        print('REG[' + monitor_command[3:].strip()+'] = ' +
              str(chip.REGISTERS[register]))
        return True, monitor, monitor_command, opcode, breakout_prompt
    if monitor_command[:1] == 'b':
        bp = monitor_command.split()[1]
        breakpoints.append(bp)
        print('Breakpoint set at address ' + bp)
        return True, monitor, monitor_command, opcode, classic_prompt
    if monitor_command == 'off':
        return False, False, '', opcode, classic_prompt
    if monitor_command == 'q':
        return None, False, monitor_command, 256, classic_prompt

    return -1, '', '', 0, None


def retrieve(inputfile: str, chip: Processor,
             quiet: bool) -> Tuple[str, int, list]:
    """
    Pass-thru function for the "reload" function.

    Parameters
    ----------
    inputfile: str, mandatory
        filename of a .obj file

    chip : Processor, mandatory
        The instance of the processor containing the registers, accumulator etc

    quiet : bool, mandatory
        Quiet mode on/off

    Returns
    -------
    m: str
        rom or ram (depending on the target memory space)

    p: int
        location to commence execution of the assembled program

    lbls: list
        labels returned from an object module
    Raises
    ------
    N/A

    Notes
    -----
    No added value in this function, simply a pass-thru.

    """
    m, p, lbls = reload(inputfile, chip, quiet)
    return m, p, lbls
