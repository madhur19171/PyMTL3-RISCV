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
JALR = int('1100111', 2)  # 103  This instructionIn jumps to an address specified by a register,


class Decoder(Component):

    def construct(s):
        s.writeEnable                   = InPort(1)
        s.instructionIn                 = InPort(32)
        s.func7                         = OutPort(7)
        s.opcode                        = OutPort(7)
        s.func3                         = OutPort(3)
        s.immediate                     = OutPort(32)
        s.programCounter                = OutPort(32)
        s.DecoderDataOutSourceRegister1 = OutPort(32)
        s.DecoderDataOutSourceRegister2 = OutPort(32)
        s.dataInSourceRegister1 = Wire(32)
        s.dataInSourceRegister2 = Wire(32)
        # Implement the logic
        s.sourceRegister1 = Wire(5)
        s.sourceRegister2 = Wire(5)
        s.destinationRegister = Wire(5)


        s.RegisterFile = RegisterFile()
        s.RegisterFile.readEnable //= 1
        s.RegisterFile.writeEnable //= s.writeEnable
        s.RegisterFile.AddrSourceRegister1 //= s.sourceRegister1
        s.RegisterFile.AddrSourceRegister2 //= s.sourceRegister2
        s.RegisterFile.AddrDestinationRegister //= s.destinationRegister
        #s.RegisterFile.dataOutSourceRegister1 //= s.dataInSourceRegister1
        #s.RegisterFile.dataOutSourceRegister2 //= s.dataInSourceRegister2

        @update
        def decode():
            # Extract fields
            s.programCounter @= s.instructionIn
            s.func7 @= s.instructionIn[25:32]
            s.sourceRegister2 @= s.instructionIn[20:25]
            s.sourceRegister1 @= s.instructionIn[15:20]
            s.func3 @= s.instructionIn[12:15]
            s.destinationRegister @= s.instructionIn[7:12]
            s.opcode @= s.instructionIn[0:7]

            s.dataInSourceRegister1 @= s.RegisterFile.dataOutSourceRegister1
            s.dataInSourceRegister2 @= s.RegisterFile.dataOutSourceRegister2

            s.DecoderDataOutSourceRegister1 @= s.dataInSourceRegister1
            s.DecoderDataOutSourceRegister2 @= s.dataInSourceRegister2

            # Decode instructionIn
            if s.opcode == OP_immediate:
                # ADDI, SLTI, SLTIU, XORI, ORI, ANDI, SLLI, SRLI, SRAI
                if (s.func3 == 1) | (s.func3 == 5):
                    s.immediate @= sext(s.instructionIn[20:25], 32)
                else:
                    s.immediate @= sext(s.instructionIn[20:32], 32)

            elif s.opcode == LOAD:
                # LB, LH, LW, LBU, LHU
                s.immediate @= sext(s.instructionIn[20:32], 32)

            elif s.opcode == STORE:
                # SB, SH, SW
                s.immediate @= sext(concat(s.instructionIn[7:12] , s.instructionIn[25:32]), 32)

            elif s.opcode == BRANCH:
                # BEQ, BNE, BLT, BGE, BLTU, BGEU
                s.immediate @= sext(concat(s.instructionIn[31], s.instructionIn[7], s.instructionIn[25:30], s.instructionIn[8:11]),32)

            elif s.opcode == LUI:
                # LUI
                s.immediate @= sext(s.instructionIn[12:32], 32)

            elif s.opcode == JAL:
                # JAL
                s.immediate @= sext(concat(s.instructionIn[12] ,s.instructionIn[20:31], s.instructionIn[12:20], s.instructionIn[31]),32)

            elif s.opcode == JALR:
                # JALR
                s.immediate @= sext(s.instructionIn[20:32], 32)
