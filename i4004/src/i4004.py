
from opcodes import i4004

class processor:

    # i4004 Processor characteristics
    MAX_4_BITS = 15             #    Maximum value 4 bits can hold
    MSB = 8                     #    Most significant bit value (4-bit)
    
    MEMORY_SIZE_RAM = 4096      # Number of 4-bit words in RAM
    MEMORY_SIZE_ROM = 4096      # Number of 4-bit words in ROM
    MEMORY_SIZE_DRAM = 4096     # Number of 4-bit words in PRAM
    STACK_SIZE = 3              # Number of 12-bit registers in the stack
    NO_REGISTERS = 16           # Number of registers
    NO_DRB = 8                  # Number of Data RAM Banks (0-7)
    NO_COMMAND_REGISTERS = 4    # Number of command registers    

    # Creation of processor internals

    ACCUMULATOR = 0         # Initialise the accumulator
    ACBR = 0                # Accumulator Buffer Register
    CARRY = 0               # Reset the carry bit
    COMMAND_REGISTERS = []  # Command Register (Select Data RAM Bank)
    CURRENT_DRAM_BANK = 0   # Current Data RAM Bank
    PROGRAM_COUNTER = 0     # Program Counter
    RAM = []                # RAM
    ROM = []                # ROM
    REGISTERS = []          # Registers
    PRAM = [[],[],[]]       # Program RAM
    STACK = []              # The stack
    STACK_POINTER = 2       # Stack Pointer
    
    # Instruction table
    INSTRUCTIONS = i4004.opcodes

    # Initialisation methods

    def __init_ram(self):
        for _i in range(self.MEMORY_SIZE_RAM):
            self.RAM.append(0)

    def __init_command_registers(self):
        for _i in range(self.NO_COMMAND_REGISTERS ):
            self.COMMAND_REGISTERS.append(0)

    def __init_registers(self):
        for _i in range(self.NO_REGISTERS):
            self.REGISTERS.append(0)

    def __init_stack(self):
        for _i in range(self.STACK_SIZE):
            self.STACK.append(0)
    
    def __init_rom(self):
        for _i in range(self.MEMORY_SIZE_ROM):
            self.ROM.append(0)

    def __init_dram(self):
        self.PRAM = [[[0 for _j in range(7)] for _k in range(255)] for _l in range(3)]


    # Sub-operation methods

    def set_carry(self):
        # Set the carry bit
        self.CARRY = 1
        return self.CARRY

    def reset_carry(self):
        # Reset the carry bit
        self.CARRY = 0
        return self.CARRY

        
    # Miscellaneous read/write operations

    def read_complement_carry(self):
        # Return the complement of the carry bit
        return 1 if self.CARRY == 0 else 0

    def write_to_stack(self, value: int):
        # Note that the stack pointer begins at 2, and then moves toward 0
        #
        #     After 2 writes            After 3 writes            After 3 writes
        #     +------------+            +------------+            +------------+
        #     |     a      |            |      a     |  <---SP    |      d     |
        #     |     b      |            |      b     |            |      b     |  <---SP
        #     |            |  <---SP    |      c     |            |      c     |
        #     +------------+            +------------+            +------------+
        # 
        # Note that after 3 writes, address "a" is lost

        self.STACK[self.STACK_POINTER] = value
        self.STACK_POINTER = self.STACK_POINTER - 1 
        if (self.STACK_POINTER == -1 ):
            self.STACK_POINTER = 2
        return None
 

    def read_from_stack(self):
        # Note that the stack pointer begins at 2, and then moves toward 0
        #
        #     First Read                Second Read               Third Read
        #     +------------+            +------------+            +------------+
        #     |     d      |  <---SP    |      d     |            |      d     |
        #     |     b      |            |      b     |            |      b     |  <---SP
        #     |     c      |            |      c     |  <---SP    |      c     |
        #     +------------+            +------------+            +------------+
        # 
       
        value = self.STACK[self.STACK_POINTER]
        self.STACK_POINTER = self.STACK_POINTER + 1 
        if (self.STACK_POINTER == 2 ):
            self.STACK_POINTER = 0
        return value

    # Utility operations 


    def ones_complement(self, value: str):
        # Perform a one's complement
        # i.e. invert all the bits
        binary = bin(value)[2:].zfill(4)
        ones = ''
        for x in range(4):
            if (binary[x] == '1'):
                ones = ones + '0'
            else:
                ones = ones + '1'   
        return ones


    def decimal_to_binary(self, decimal: int):
        # Convert decimal to binary
        binary = bin(decimal)[2:].zfill(4)
        return binary
    

    def binary_to_decimal(self, binary: str):
        # Convert binary to decinal
        decimal = 0
        for digit in binary:
            decimal = decimal * 2 + int(digit)
        return decimal

    # Initialise processor

    def __init__(self):
        # Initialise all the internals of the processor
        self.ACCUMULATOR = 0
        self.ACBR = 0
        self.CURRENT_RAM_BANK = 0
        self.PROGRAM_COUNTER == 0
        self.STACK_POINTER == 0
        self.__init_stack()
        self.__init_command_registers()
        self.__init_registers()
        self.__init_dram()
        self.__init_ram()
        self.__init_rom()
        self.reset_carry()



    ############################################################################
    #                                                                          #
    #            .-.                                                           #
    #           (._.)        ,--.      .-.      .-.        ,--.                #
    #            .-.        /   |    /    \   /    \      /   |                #
    #            | |       / .' |   |  .-. ; |  .-. ;    / .' |                #
    #            | |     / /  | |   | |  | | | |  | |  / /  | |                #
    #            | |      / / | |   | |  | | | |  | |   / / | |                #
    #            | |    /  `--' |-. | |  | | | |  | | /  `--' |-.              #
    #            | |    `-----| |-' | '  | | | '  | | `-----| |-'              #
    #            | |          | |   '  `-' / '  `-' /       | |                #
    #           (___)        (___)   `.__,'   `.__,'       (___)               #
    #                                                                          #
    #     _           _                   _   _                        _       #
    #    (_)_ __  ___| |_ _ __ _   _  ___| |_(_) ___  _ __    ___  ___| |_     #
    #    | | '_ \/ __| __| '__| | | |/ __| __| |/ _ \| '_ \  / __|/ _ \ __|    #
    #    | | | | \__ \ |_| |  | |_| | (__| |_| | (_) | | | | \__ \  __/ |_     #
    #    |_|_| |_|___/\__|_|   \__,_|\___|\__|_|\___/|_| |_| |___/\___|\__|    # 
    #                                                                          #
    ############################################################################

    """
    Abbreviations used in the descriptions of each instruction's actions:

            (    )	    the content of
            -->	        is transferred to
            ACC	        Accumulator (4-bit)
            CY	        Carry/link Flip-Flop
            ACBR	    Accumulator Buffer Register (4-bit)
            RRRR	    Index register address
            RRR	        Index register pair address
            PL	        Low order program counter Field (4-bit)
            PM	        Middle order program counter Field (4-bit)
            PH	        High order program counter Field (4-bit)
            ai	        Order i content of the accumulator
            CMi	        Order i content of the command register
            M	        RAM main character location
            MSi	        RAM status character i
            DB (T)	    Data bus content at time T
            Stack	    The 3 registers in the address register other than the program counter
    """
    # Operators

    # One Word Machine Instructions

    def nop(self):
        """
        Name:           No Operation
        Function:       No operation performed.
        Syntax:         NOP
        Assembled:      0000 0000
        Symbolic:       Not applicable
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   Not Applicable
        """

        return self

    def ldm(self, operand:int):
        """
        Name:           Load Accumulator Immediate
        Function:       The 4 bits of immediate data are loaded into the accumulator.
        Syntax:         LDM <value>
        Assembled:      1101 <DDDD>
        Symbolic:       DDDD --> ACC
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry bit is not affected.
        """

        self.ACCUMULATOR = operand
        return self.ACCUMULATOR

    def ld(self, register:int):
        """
        Name:           Load index register to Accumulator
        Function:       The 4 bit content of the designated index register (RRRR) is loaded into accumulator.
                        The previous contents of the accumulator are lost.
        Syntax:         LD <value>
        Assembled:      1010 <RRRR>
        Symbolic:       (RRRR) --> ACC
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry bit is not affected.
        """

        self.ACCUMULATOR = self.REGISTERS[register]
        return self.ACCUMULATOR
   
    
    def xch(self, register:int):
        """
        Name:           Exchange index register and accumulator
        Function:       The 4 bit content of designated index register is loaded into the accumulator.
                        The prior content of the accumulator is loaded into the designed register.
        Syntax:         XCH <register>
        Assembled:      1011 <RRRR>
        Symbolic:       (ACC) --> ACBR, (RRRR) --> ACC, (ACBR) --> RRRR
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry bit is not affected.
        """

        self.ACBR = self.ACCUMULATOR
        self.ACCUMULATOR = self.REGISTERS[register]
        self.REGISTERS[register] = self.ACBR
        return self.ACCUMULATOR, self.REGISTERS

  
    def add(self, register:int):
        """
        Name:           Add index register to accumulator with carry
        Function:       The 4 bit content of the designated index register is added to the content of the accumulator with carry.
                        The result is stored in the accumulator. (Note this means the carry bit is also added)
        Syntax:         ADD <register>
        Assembled:      1000 <RRRR>
        Symbolic:       (RRRR) + (ACC) + (CY) --> ACC, CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry/link is set to 1 if a sum greater than MAX_4_BITS was generated to indicate a carry out; 
                        otherwise, the carry/link is set to 0. The 4 bit content of the index register is unaffected.
        """
        
        self.ACCUMULATOR = self.ACCUMULATOR + self.REGISTERS[register] + self.read_carry()
        # Check for carry bit set/reset when an overflow is detected
        # i.e. the result is more than a 4-bit number (MAX_4_BITS)
        if (self.ACCUMULATOR > self.MAX_4_BITS ):
            self.ACCUMULATOR = self.MAX_4_BITS  - self.MAX_4_BITS - 1 
            self.set_carry()
        else:
            self.reset_carry()
        return self.ACCUMULATOR, self.CARRY


    def sub(self, register:int):
        """
        Name:           Subtract index register from accumulator with borrow    
        Function:       The 4 bit content of the designated index register is complemented (ones complement) and 
                        added to content of the accumulator with borrow and the result is stored in the accumulator.
        Syntax:         SUB <register>
        Assembled:      1001 <RRRR>
        Symbolic:       (ACC) + ~(RRRR) + (CY) --> ACC, CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   If a borrow is generated, the carry bit is set to 0; otherwise, it is set to 1.
                        The 4 bit content of the index register is unaffected.        
        """

        carry = self.read_complement_carry()
        self.ACCUMULATOR = self.ACCUMULATOR + self.binary_to_decimal(self.ones_complement(self.REGISTERS[register])) + carry

        # Check for carry bit set/reset when borrow (overflow) is detected
        # i.e. the result is more than a 4-bit number (MAX_4_BITS)
        if (self.ACCUMULATOR > self.MAX_4_BITS ):
            self.ACCUMULATOR = self.ACCUMULATOR - self.MAX_4_BITS - 1
            self.set_carry()
        else:
            self.reset_carry()
        return self.ACCUMULATOR, self.CARRY


    def inc(self, register:int):
        """
        Name:           Increment index register
        Function:       The 4 bit content of the designated index register is incremented by 1. 
                        The index register is set to zero in case of overflow.
        Syntax:         INC <register>
        Assembled:      0110 <RRRR>
        Symbolic:       (RRRR) +1 --> RRRR
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry bit is not affected.
        """

        self.REGISTERS[register] = self.REGISTERS[register] + 1
        if (self.REGISTERS[register] > self.MAX_4_BITS ):
            self.REGISTERS[register] = self.MAX_4_BITS - self.REGISTERS[register]
        return self.REGISTERS[register]


    def bbl(self):
        return None


    def jin(self):
        return None


    def src(self):
        return None


    def fin(self, registerpair:int):
        """
        Name:           Fetch indirect from ROM
        Function:       The 8 bit content of the 0 index register pair (0000) (0001)
                        is sent out as an address in the same page where the FIN 
                        instruction is located. The 8 bit word at that location is 
                        loaded into the designated index register pair.
                        The program counter is unaffected; after FIN has been executed 
                        the next instruction in sequence will be addressed. 
                        The content of the 0 index register pair is unaltered unless 
                        index register 0 was designated.
        Syntax:         FIN
        Assembled:      0011 RRRO
        Symbolic:       (PH) (0000) (0001) --> ROM address
                        (OPR) --> RRRO
                        (OPA) --> RRR1
        Execution:      1 word, 16-bit code and an execution time of 21.6 usec..
        Side-effects:   Not Applicable
        Exceptions:     a) Although FIN is a 1-word instruction, its execution requires 
                            two memory cycles (21.6 psec).
                        b) When FIN is located at address (PH) 1111 1111 data will 
                            be fetched from the next page(ROM) in sequence and not 
                            from the same page(ROM) where the FIN instruction is 
                            located. That is, next address is (PH + 1) (0000) (0001) 
                            and not (PH) (0000) (0001).
        """

        ##### NEED TO IMPLEMENT EXCEPTION B #####
        value = self.RAM[self.REGISTERS[1] + (self.REGISTERS[0] << 4)]
        self.REGISTERS[registerpair] = (value >> 4 )  & 15
        self.REGISTERS[registerpair + 1] = value & 15
        return self.REGISTERS[registerpair], self.REGISTERS[registerpair+1]

    # 2-word Instructions

    def fim(self, registerpair:int, value:int):
        """
        Name:           Fetched immediate from ROM
        Function:       The 2nd word represents 8-bits of data 
                        which are loaded into the designated index register pair.
        Syntax:         FIM
        Assembled:      0010 RRR0
                        DDDD2  DDDD1
        Symbolic:       DDDD --> RRR0, DDDD1 --> RRR1
        Execution:      2 words, 16-bit code and an execution time of 21.6 usec..
        Side-effects:   Not Applicable
        """

        self.REGISTERS[registerpair] = (value >> 4 )  & 15
        self.REGISTERS[registerpair+1] = value & 15
        return self.REGISTERS

    # Accumulator Group Instructions

    def clb(self):
        """
        Name:           Clear Both
        Function:       Set accumulator and carry/link to 0.
        Syntax:         CLB
        Assembled:      1111 0000
        Symbolic:       0 --> ACC, 0 --> CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   Not Applicable
        """

        self.ACCUMULATOR = 0
        self.reset_carry()
        return self.ACCUMULATOR, self.CARRY


    def clc(self):
        """
        Name:           Clear Carry
        Function:       Set carry/link to 0.
        Syntax:         CLC
        Assembled:      1111 0001
        Symbolic:       0 --> CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   Not Applicable
        """

        self.reset_carry()
        return self.CARRY

    def cmc(self):
        """
        Name:           Complement carry
        Function:       The carry/link content is complemented.
        Syntax:         CLC
        Assembled:      1111 0011
        Symbolic:       ~(CY) --> CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   Not Applicable
        """

        if (self.CARRY == 1):
            self.reset_carry()
        else:
            self.set_carry()
        return self.CARRY


    def stc(self):
        """
        Name:           Set Carry
        Function:       Set carry/link to 1.
        Syntax:         STC
        Assembled:      1111 1010
        Symbolic:       1 --> CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   Not Applicable
        """

        self.set_carry()
        return self.CARRY


    def cma(self):
        """
        Name:           Complement Accumulator
        Function:       The content of the accumulator is complemented. The carry/link is unaffected.
        Syntax:         CMA
        Assembled:      1111 0100
        Symbolic:       ~a3 ~a2 ~a1 ~a0 --> ACC
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   Not Applicable
        """

        self.ACCUMULATOR = self.ones_complement(self.ACCUMULATOR)
        return self.ACCUMULATOR


    def iac(self):
        """
        Name:           Increment accumulator
        Function:       The content of the accumulator is incremented by 1.
        Syntax:         IAC
        Assembled:      1111 0010
        Symbolic:       (ACC) +1 --> ACC
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   No overflow sets the carry/link to 0; overflow sets the carry/link to a 1.
        """

        self.ACCUMULATOR = self.ACCUMULATOR + 1
        if (self.ACCUMULATOR > self.MAX_4_BITS ):
            self.ACCUMULATOR = self.MAX_4_BITS - self.ACCUMULATOR
            self.set_carry()
        else:
            self.reset_carry()
        return self.ACCUMULATOR, self.CARRY


    def dac(self):
        """
        Name:           Decrement accumulator
        Function:       The content of the accumulator is decremented by 1.
        Syntax:         DAC
        Assembled:      1111 1000
        Symbolic:       (ACC) -1 --> ACC
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   A borrow sets the carry/link to 0; no borrow sets the carry/link to a 1.
        """

        self.ACCUMULATOR = self.ACCUMULATOR + 15
        if (self.ACCUMULATOR > self.MAX_4_BITS ):
            self.ACCUMULATOR = self.MAX_4_BITS - self.ACCUMULATOR
            self.set_carry()
        else:
            self.reset_carry()
        return self.ACCUMULATOR, self.CARRY


    def ral(self):
        """
        Name:           Rotate left
        Function:       The content of the accumulator and carry/link are rotated left.
        Syntax:         RAL
        Assembled:      1111 0101
        Symbolic:       C0 --> a0, a(i) --> a(i+1), a3 -->CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry bit will be set to the highest significant bit of the accumulator.
        """

        # Store Carry bit
        C0 = self.read_carry()
        # Shift left
        self.ACCUMULATOR = self.ACCUMULATOR * 2
        # Set carry bit correctly
        if (self.ACCUMULATOR >= self.MAX_4_BITS):
                self.set_carry()
        else:
            self.reset_carry()
        # If necessary remove non-existent bit 5
        if (self.ACCUMULATOR > self.MAX_4_BITS ):
            self.ACCUMULATOR = self.ACCUMULATOR - self.MAX_4_BITS - 1
        # Add ooriginal carry bit
        self.ACCUMULATOR = self.ACCUMULATOR + C0
        return self.ACCUMULATOR, self.CARRY


    def rar(self):
        """
        Name:           Rotate right
        Function:       The content of the accumulator and carry/link are rotated right.
        Syntax:         RAR
        Assembled:      1111 0110
        Symbolic:       a0 --> CY, a(i) --> a(i-1), C0 -->a3
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry bit will be set to the lowest significant bit of the accumulator.
        """

        # Store Carry bit
        C0 = self.read_carry()
        # Set carry bit coorrectly
        if (self.ACCUMULATOR % 2 == 0):
            self.reset_carry()
        else:
            self.set_carry() 
        # Shift right
        self.ACCUMULATOR = self.ACCUMULATOR // 2 
        # Add carry to high-order bit of accumulator
        self.ACCUMULATOR = self.ACCUMULATOR + (C0 * self.MSB)
        return self.ACCUMULATOR, self.CARRY


    def tcc(self):
        """
        Name:           Transmit carry and clear
        Function:       The accumulator is cleared. 
                        The least significant position of the accumulator is set to the value of the carry/link.
        Syntax:         TCC
        Assembled:      1111 0111
        Symbolic:       0 --> ACC, (CY) --> a0, 0 --> CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry bit will be set to the 0.
        """

        self.ACCUMULATOR = 0
        self.ACCUMULATOR = self.read_carry()
        self.reset_carry()
        return self.ACCUMULATOR, self.CARRY


    def daa(self):
        """
        Name:           Decimal adjust accumulator
        Function:       The accumulator is incremented by 6 if 
                        either the carry/link is 1 or if the accumulator content is greater than 9.        
        Syntax:         DAA
        Assembled:      1111 1011
        Symbolic:       (ACC) + (0000 or 0110) --> ACC
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry/link is set to a 1 if the result generates a carry, otherwise it is unaffected.
        """

        if (self.read_carry == 1 or self.ACCUMULATOR > 9):
            self.ACCUMULATOR = self.ACCUMULATOR + 6
            if (self.ACCUMULATOR > self.MAX_4_BITS ):
                self.ACCUMULATOR = self.MAX_4_BITS  - self.MAX_4_BITS 
            self.set_carry()
        else:
            self.reset_carry()
        return self.ACCUMULATOR, self.CARRY

    def tcs(self):
        """
        Name:           Transfer Carry Subtract
        Function:       The accumulator is set to 9 if the carry/link is 0.
                        The accumulator is set to 10 if the carry/link is a 1.    
        Syntax:         TCS
        Assembled:      1111 1001
        Symbolic:       1001 --> ACC if (CY) = 0
                        1010 --> ACC if (CY) = 1
                        0 --> CY
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry/link is set to 0.
        """

        if (self.read_carry() == 0 ):
            self.ACCUMULATOR = 9
        else:
            self.ACCUMULATOR = 10
        self.reset_carry()
        return self.ACCUMULATOR, self.CARRY

    def kbp(self):
        """
        Name:           Keyboard process
        Function:       A code conversion is performed on the accumulator content, from 1 out of n to binary code. 
                        If the accumulator content has more than one bit on, the accumulator will be set to 15 
                        (to indicate error) - conversion table below
        Syntax:         KBP
        Assembled:      1111 1100
        Symbolic:       (ACC) --> KBP, ROM --> ACC
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   The carry/link is unaffected.


                        (ACC)           (ACC)
                        before          after
                         KBP	  	     KBP
                         0000	---->	0000
                         0001	---->	0001
                         0010	---->	0010
                         0100	---->	0011
                         1000	---->	0100
                         0011	---->	1111    Error
                         0101	---->	1111    Error
                         0110	---->	1111    Error
                         0111	---->	1111    Error
                         1001	---->	1111    Error
                         1010	---->	1111    Error
                         1011	---->	1111    Error
                         1100	---->	1111    Error
                         1101	---->	1111    Error
                         1110	---->	1111    Error
                         1111	---->	1111    Error
        """
        if (self.ACCUMULATOR == 0 or self.ACCUMULATOR == 1 or self.ACCUMULATOR == 2):
            return self.ACCUMULATOR
        
        if (self.ACCUMULATOR == 4):
            self.ACCUMULATOR = 3
            return self.ACCUMULATOR
        
        if (self.ACCUMULATOR == 8):
            self.ACCUMULATOR = 4
            return self.ACCUMULATOR
        
        # Error
        self.ACCUMULATOR = 15 
        return self.ACCUMULATOR


    def dcl(self):
        """
        Name:           Designate command line
        Function:       The content of the three least significant accumulator bits is transferred to the 
                        comand control register within the CPU. This instruction provides RAM bank 
                        selection when multiple RAM banks are used.
                        (If no DCL instruction is sent out, RAM Bank number zero is automatically selected 
                        after application of at least one RESET). See below for RAM Bank selection table.
                        DCL remains latched until it is changed.
        Syntax:         DCL
        Assembled:      1111 1101
        Symbolic:       a0 --> CM0, a1 --> CM1, a2 --> CM2
        Execution:      1 word, 8-bit code and an execution time of 10.8 usec.
        Side-effects:   Not Applicable

                        The selection is made according to the following table.
                        (ACC)	CM-RAMi                     Enabled	Bank No.
                        -----	------------------------	------------
                        X000	CM-RAM0	                    Bank 0
                        X001	CM-RAM1	                    Bank 1
                        X010	CM-RAM2	                    Bank 2
                        X100	CM-RAM3	                    Bank 3
                        X011	CM-RAM1, CM-RAM1	        Bank 4
                        X101	CM-RAM1, CM-RAM3	        Bank 5
                        X110	CM-RAM2, CM-RAM3	        Bank 6
                        X111	CM-RAM1, CM-RAM2, CM-RAM3	Bank 7
        """

        ACC = self.ACCUMULATOR
        if (ACC == 0):
            self.COMMAND_REGISTERS[0] = 0
            self.COMMAND_REGISTERS[1] = 0
            self.COMMAND_REGISTERS[2] = 0
            self.COMMAND_REGISTERS[3] = 0
            self.CURRENT_RAM_BANK = 0
            return self.COMMAND_REGISTERS, self.CURRENT_RAM_BANK
        
        self.COMMAND_REGISTERS[1] = ACC & 1
        self.COMMAND_REGISTERS[2] = ACC & 2
        self.COMMAND_REGISTERS[3] = ACC & 4
        self.CURRENT_RAM_BANK = ACC & 7
        return self.COMMAND_REGISTERS, self.CURRENT_RAM_BANK



    # Output Methods

    def read_all_registers(self):
        return(self.REGISTERS)

    def read_all_ram(self):
        return(self.RAM)

    def read_all_rom(self):
        return(self.ROM)

    def read_all_pram(self):
        return(self.PRAM)

    def read_accumulator(self):
        return(self.ACCUMULATOR)
    
    def read_current_ram_bank(self):
        return(self.CURRENT_RAM_BANK)

    def read_carry(self):
        return(self.CARRY)

# Mnemonic link: http://e4004.szyc.org/iset.html


def execute(chip, location, PC, monitor):
    _TPS = []
    if (location == 'rom'):
        _TPS = chip.ROM
    else:
        _TPS = chip.RAM
    PC = 0
    opcode = 0
    while opcode != 255:  # pseudo-opcode (directive) for "end"
        custom_opcode = False
        OPCODE = _TPS[PC]
        if (OPCODE == 255): # pseudo-opcode (directive "end" - stop program)
            print('           end')
            break
        opcodeinfo  = next((item for item in chip.INSTRUCTIONS if item['opcode'] == OPCODE), None)
        exe = opcodeinfo['mnemonic']
        words = opcodeinfo['words']
        if (words == 2):
            next_word = str(_TPS[PC+1 ])
            OPCODE = str(OPCODE) + ',' + next_word
        
        # Only mnemonic with 2 characters - fix
        if (exe[:3]=='ld '):
            exe = exe[:2] + exe[3:]
        
        # Ensure that the correct arguments are passed to the operations
        if (exe[:6]=='fim(rp'):
            custom_opcode = True
            value = str(_TPS[PC+1 ])
            cop = exe.replace('data8',value)
            exe = exe.replace('rp','').replace('data8)','')
            exe = exe + value + ')'

        if (custom_opcode):
            custom_opcode = False
            print('  {:>7}  {:<10}'.format(OPCODE,cop))
        else:
            print('  {:>7}  {:<10}'.format(OPCODE,exe))

        exe = 'chip.' + exe
        eval(exe)
        # Increment Program Counter by the correct number of words
        PC = PC + words
        monitor_command = 'none'
        if (monitor):
            while (monitor_command != ''):
                monitor_command = input('>> ').lower()
                if (monitor_command == 'regs'):
                    print('[0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15]')
                    print('[----------------------------------------------]')
                    print(chip.REGISTERS)
                    continue
                if (monitor_command == 'pc'):
                    print('PC = ',PC)
                if (monitor_command[:3] == 'reg'):
                    register = int(monitor_command[3:])
                    print('REG['+ monitor_command[3:].strip()+'] = ' + str(chip.REGISTERS[register]))
                if (monitor_command == 'acc'):
                    print('ACC =',chip.read_accumulator())
                if (monitor_command == 'off'):
                    monitor_command = ''
                    monitor = False
                
    return True

def match_label(_L,label: str, address):
    for _i in range(len(_L)):
        if (_L[_i]['label']==label):
            _L[_i]['address'] = address
    return _L

def add_label(_L,label: str):
    label_exists  = next((item for item in _L if str(item["label"]) == label), None)
    if not label_exists:
        _L.append({'label':label,'address':-1})
    else:
        return (-1)
    print(_L)
    return _L

def assemble(program_name: str, chip):
    # Reset label table for this program
    _LABELS=[]

    # Reset temporary_program_store
    TPS = []
    TPS_SIZE = max([chip.MEMORY_SIZE_ROM, chip.MEMORY_SIZE_RAM,chip.MEMORY_SIZE_RAM])
    for _i in range(TPS_SIZE):
        TPS.append(0)

    program = open(program_name, 'r')
    print()
    print()
    print('Program Code:', program_name)
    print()
    print('Label      Address    Assembled             Dec        Line     Op/Operand')
    ORG_FOUND = False
    location = ''
    count = 0
    ERR = False
    
    TFILE = []
    TFILE_SIZE = max([chip.MEMORY_SIZE_ROM, chip.MEMORY_SIZE_RAM,chip.MEMORY_SIZE_RAM])
    for _i in range(TFILE_SIZE):
        TFILE.append('')

    p_line = 0
    while True:
        line = program.readline()
        # if line is empty
        # end of file is reached
        if not line:
            break
        else:
            x = line.split()
            if (x[0][-1] == ','):
                success = add_label(_LABELS,x[0])
                if success == -1:
                    print()
                    print('FATAL: Pass 1: Duplicate label: ' + x[0] + ' at line '+ str(p_line+1))
                    ERR = True
                    break
            line = line.strip()
            TFILE[p_line] = line
            p_line = p_line + 1
    program.close()
    if ERR:
        print("Program Assembly halted")
        print()
        return False
    count=0
    while True:
        line = TFILE[count].strip()
        if (len(line)==0):
            break
        x = line.split()
        label = ''
        if (line[0] == '/'):
            print('{:<10} {:>47}      {}'.format(label,str(count),line))
            pass
        else:
            if (len(line) > 0):
                opcode = x[0]
                opcodeinfo  = next((item for item in chip.INSTRUCTIONS if str(item["mnemonic"])[:3] == opcode), None)
                if (opcode in ['org','end']) or ( opcode != None):
                    if (opcode in ['org','end']):
                        if (opcode == 'org'):
                            ORG_FOUND = True
                            print('{:<10} {:>47}      {:<3} {:<3}'.format(label,str(count),opcode,str(x[1])))
                            if (x[1] == 'rom') or (x[1] == 'ram'):
                                location = x[1]
                                address = 0
                        if (opcode == 'end'):
                            print('{:<10} {:>47}      {:<14}'.format(label,str(count),opcode))
                            TPS[address] = 255 # pseudo-opcode (directive "end")
                            break
                        pass
                    else:
                        if (ORG_FOUND is True):
                            if (x[0][-1] == ','):
                                label = x[0]
                                match_label(_LABELS,label,address)
                                for _i in range(len([x])-1):
                                    x[_i] = x[_i + 1]
                                x.pop(len([x])-1)
                            opcode = x[0]
                            address_left = bin(address)[2:].zfill(8)[:4]
                            address_right = bin(address)[2:].zfill(8)[4:]
                            # Check for operand(s)
                            if (len(x) == 2):
                                # Operator and operand
                                if (opcode == 'ld'): # pad out for the only 2-character mnemonic
                                    opcode = 'ld '
                                fullopcode = opcode + '(' + x[1] + ')'
                                opcodeinfo  = next((item for item in chip.INSTRUCTIONS if item["mnemonic"] == fullopcode), None)
                                bit1 = opcodeinfo['bits'][0]
                                bit2 = opcodeinfo['bits'][1]
                                TPS[address] = opcodeinfo['opcode']
                                print('{:<10} {} {}  {} {}   {:>13} {:>10}      {:<3} {:<3}'.format(label,address_left,address_right,bit1, bit2,TPS[address], str(count),opcode,str(x[1])))
                                address = address + opcodeinfo['words']
                            if (len(x) == 1):
                                # Only operator
                                bit1 = opcodeinfo['bits'][0]
                                bit2 = opcodeinfo['bits'][1]
                                TPS[address] = opcodeinfo['opcode']
                                print('{:<10} {} {}  {} {}   {:>18} {:>5}      {:<3}'.format(label,address_left, address_right,bit1,bit2,TPS[address],str(count),opcode))
                                address = address + opcodeinfo['words']
                            if (len(x) == 3):
                                # Operator and 2 operands
                                d_type = ''
                                if (int(x[2]) <= 256):
                                    d_type = 'data8'
                                val_left = bin(int(x[2]))[2:].zfill(8)[:4]
                                val_right = bin(int(x[2]))[2:].zfill(8)[4:]
                                fullopcode = opcode + "(" + x[1] + "," + d_type +  ")"
                                opcodeinfo  = next((item for item in chip.INSTRUCTIONS if item["mnemonic"] == fullopcode), None)
                                bit1 = opcodeinfo['bits'][0]
                                bit2 = opcodeinfo['bits'][1]
                                TPS[address] = opcodeinfo['opcode']
                                TPS[address+1]=int(x[2])
                                print('{:<10} {} {}  {} {}  {} {}   {:>3} {:>5}      {:<3} {:<3} {:<3}'.format(label,address_left,address_right,bit1, bit2, val_left,val_right, str(TPS[address]) + ", " + str(TPS[address+1]), str(count),opcode,str(x[1]), str(x[2])))
                                address = address + opcodeinfo['words']    
                        else:
                            print()
                            print("FATAL: Pass 2:  No 'org' found at line: ", count + 1)
                            ERR = True
                            break    
                else:
                    print()
                    print("'FATAL: Pass 2:  Invalid mnemonic '",opcode,"' at line: ", count + 1)
                    ERR = True
                    break
        count = count + 1

    if ERR:
        print("Program Assembly halted")
        return False
    print()
    
    if (location == 'rom'):
        chip.ROM = TPS
    
    if (location == 'ram'):
        chip.RAM = TPS

    print('Labels:')
    print('Address   Label')
    for _i in range(len(_LABELS)):
        print('{:>5}     {}'.format(_LABELS[_i]['address'],_LABELS[_i]['label']))
    return True


chip = processor()
chip.RAM[173]=28

result = assemble('example.asm',chip)
if result:
    print('EXECUTING : ')
    print()
    execute(chip, 'rom', 0, True)
    print()
    print('Accumulator : ',chip.read_accumulator())
    print('              ', chip.decimal_to_binary(chip.read_accumulator()))
    print('              ', chip.read_current_ram_bank())
    print()
