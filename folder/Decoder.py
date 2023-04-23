from RegisterFile import RegisterFile
from pymtl3 import *

OP_immediate = int('0010011', 2)  # 19 perform operations between a register and an immediateediate value
OP = int('0110011', 2)  # 51 perform operations between two registers
LOAD = int('0000011', 2)  # 3 load data from memory into a register
STORE = int('0100011', 2)  # 35 store data from a register into memory
BRANCH = int('1100011', 2)  # 99 perform conditional branches
LUI = int('0110111', 2)  # 55 loads an immediateediate value into the upper 20 bits of a register,
AUIPC = int('0010111', 2)  # 23 adds immediateediate value to the program counter, and stores the result in a register
JAL = int('1101111', 2)  # 111 jumps to an immediateediate offset relative to the program counter, and stores the return
# address in a register. The offset is signed and shifted left
# by one bit, since instructions are 4 bytes (32 bits) long and the program counter is always even.
JALR = int('1100111', 2)  # 103  This instruction jumps to an address specified by a register,
# with an immediateediate offset added to the register value,
# and stores the return address in a register. The offset is signed and can be negative.
SYSTEM = int('1110011', 2)  # 115


# These instructions trigger system calls to the operating system
# and are used for debugging and performance monitoring.


class Decoder(Component):

    def construct(s):

        # INP0RT
        s.instruction = InPort(32)
        s.dataIn = InPort(32)

        # OUTPORT
        s.opcode = OutPort(7)
        s.func7 = OutPort(7)
        s.func3 = OutPort(3)
        s.immediate = OutPort(32)
        s.programCounter = OutPort(32)
        s.dataOutSourceRegister1 = OutPort(32)
        s.dataOutSourceRegister2 = OutPort(32)
        s.sourceRegister1 = OutPort(5)
        s.sourceRegister2 = OutPort(5)
        s.destinationRegister = OutPort(5)
        s.alu = OutPort(4)
        s.write_enable = InPort(1)
        # MEMORY

        s.RegisterFile = RegisterFile()

        s.RegisterFile.readEnable //= 1
        s.RegisterFile.writeEnable //= s.write_enable
        s.RegisterFile.AddrSourceRegister1 //= s.sourceRegister1
        s.RegisterFile.AddrSourceRegister2 //= s.sourceRegister2
        s.RegisterFile.AddrDestinationRegister //= s.destinationRegister
        s.RegisterFile.dataOutSourceRegister1 //= s.dataOutSourceRegister1
        s.RegisterFile.dataOutSourceRegister2 //= s.dataOutSourceRegister2
        s.RegisterFile.dataIn //= s.dataIn

        # Implement the logic
        @update
        def decode():

            # Extract fields
            s.programCounter @= s.instruction
            s.func7 @= s.instruction[25:32]
            s.sourceRegister2 @= s.instruction[20:25]
            s.sourceRegister1 @= s.instruction[15:20]
            s.func3 @= s.instruction[12:15]
            s.destinationRegister @= s.instruction[7:12]
            s.opcode @= s.instruction[0:7]
            # s.dataIn = Wire(32)

            # Decode instruction
            if s.opcode == OP_immediate:
                # ADDI, SLTI, SLTIU, XORI, ORI, ANDI, SLLI, SRLI, SRAI
                if s.func3 == b'001' or s.func3 == b'101':
                    s.immediate @= sext(s.instruction[20:25], 32)
                else:
                    s.immediate @= sext(s.instruction[20:32], 32)

            elif s.opcode == LOAD:
                # LB, LH, LW, LBU, LHU
                s.immediate @= sext(s.instruction[20:32], 32)

            elif s.opcode == STORE:
                # SB, SH, SW
                s.immediate @= sext(concat(s.instruction[7:12], s.instruction[25:32]), 32)

            elif s.opcode == BRANCH:
                # BEQ, BNE, BLT, BGE, BLTU, BGEU
                s.immediate @= sext(
                    concat(s.instruction[31], s.instruction[7], s.instruction[25:30], s.instruction[8:11]), 12)

            elif s.opcode == LUI:
                # LUI
                s.immediate @= sext(s.instruction[12:32], 32)

            elif s.opcode == JAL:
                # JAL
                s.immediate @= sext(
                    concat(s.instruction[12], s.instruction[20:31], s.instruction[12:20], s.instruction[31]), 21)

            elif s.opcode == JALR:
                # JALR
                s.immediate @= sext(s.instruction[20:32], 12)

