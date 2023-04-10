from pymtl3 import *

OP_IMM = int('0010011', 2)  # 19 perform operations between a register and an immediate value
OP = int('0110011', 2)  # 51 perform operations between two registers
LOAD = int('0000011', 2)  # 3 load data from memory into a register
STORE = int('0100011', 2)  # 35 store data from a register into memory
BRANCH = int('1100011', 2)  # 99 perform conditional branches
LUI = int('0110111', 2)  # 55 loads an immediate value into the upper 20 bits of a register,
AUIPC = int('0010111', 2)  # 23 adds immediate value to the program counter, and stores the result in a register
JAL = int('1101111', 2)  # 111 jumps to an immediate offset relative to the program counter, and stores the return
# address in a register. The offset is signed and shifted left
# by one bit, since instructions are 4 bytes (32 bits) long and the program counter is always even.
JALR = int('1100111', 2)  # 103  This instruction jumps to an address specified by a register,
# with an immediate offset added to the register value,
# and stores the return address in a register. The offset is signed and can be negative.
SYSTEM = int('1110011', 2)  # 115
# These instructions trigger system calls to the operating system
# and are used for debugging and performance monitoring.


class RISCVDecoder(Component):

    def __init__(self):
        self.immediate = None
        self.opcode = None
        self.alu = None
        self.rd = None
        self.rs2 = None
        self.rs1 = None
        self.instr = None

    def construct(s):
        DataWidth = 32
        AluWidth = 4
        # Interface
        s.instr = InPort(DataWidth)
        s.rs1 = OutPort(5)
        s.rs2 = OutPort(5)
        s.rd = OutPort(5)
        s.immediate = OutPort(DataWidth)
        s.alu = OutPort(AluWidth)
        s.opcode = OutPort(7)

        # Implement the logic
        @update
        def decode():
            # Extract fields
            s.opcode @= s.instr[0:7]
            s.rs1 @= s.instr[15:20]
            s.rs2 @= s.instr[20:25]
            s.rd @= s.instr[7:12]
            funct3 = s.instr[12:15]
            funct7 = s.instr[25:32]

            # Initialize the ALU operation code to an invalid value
            s.alu @= 0xF

            # Decode instruction
            if s.opcode == OP_IMM:
                # ADDI, SLTI, SLTIU, XORI, ORI, ANDI, SLLI, SRLI, SRAI
                if funct3 == b'000':  # ADDI
                    s.imm @= sext(s.instr[20:32], 12)
                    s.alu @= 0b0000  # ADD
                elif funct3 == b'010':  # SLTI
                    s.imm @= sext(s.instr[20:32], 12)
                    s.alu @= 0b0110  # LT
                elif funct3 == b'011':  # SLTIU
                    s.imm @= sext(s.instr[20:32], 12)
                    s.alu @= 0b0111  # LTU
                elif funct3 == b'100':  # XORI
                    s.imm @= s.instr[20:32]
                    s.alu @= 0b1001  # XOR
                elif funct3 == b'110':  # ORI
                    s.imm @= s.instr[20:32]
                    s.alu @= 0b1101  # OR
                elif funct3 == b'111':  # ANDI
                    s.imm @= s.instr[20:32]
                    s.alu @= 0b1110  # AND
                elif funct3 == b'001':  # SLLI
                    s.imm @= s.instr[20:25]
                    s.alu @= 0b0001  # SLL
                elif funct3 == b'101':
                    if funct7 == b'0000000':  # SRLI
                        s.imm @= s.instr[20:25]
                    elif funct7 == b'0100000':  # SRAI
                        s.imm @= s.instr[20:25]
                        s.alu @= 0b1000  # SRA

            elif s.opcode == OP:
                # ADD, SUB, SLL, SLT, SLTU, XOR, SRL, SRA, OR, AND
                if funct3 == b'000':
                    if funct7 == b'0000000':  # ADD
                        s.alu @= 0b0000
                    elif funct7 == b'0100000':  # SUB
                        s.alu @= 0b0001
                elif funct3 == b'001':  # SLL
                    s.alu @= 0b0001
                elif funct3 == b'010':  # SLT
                    s.alu @= 0b0110
                elif funct3 == b'011':  # SLTU
                    s.alu @= 0b0111
                elif funct3 == b'100':  # XOR
                    s.alu @= 0b1001
                elif funct3 == b'101':
                    if funct7 == b'0000000':  # SRL
                        s.alu @= 0b1010
                    elif funct7 == b'0100000':  # SRA
                        s.alu @= 0b1000
                elif funct3 == b'110':  # OR
                    s.alu @= 0b1101
                elif funct3 == b'111':  # AND
                    s.alu @= 0b1110

            elif s.opcode == LOAD:
                # LB, LH, LW, LBU, LHU
                if funct3 == b'000':  # LB
                    s.imm @= sext(s.instr[20:32], 12)
                elif funct3 == b'001':  # LH
                    s.imm @= sext(s.instr[20:32], 12)
                elif funct3 == b'010':  # LW
                    s.imm @= sext(s.instr[20:32], 12)
                elif funct3 == b'100':  # LBU
                    s.imm @= sext(s.instr[20:32], 12)
                elif funct3 == b'101':  # LHU
                    s.imm @= sext(s.instr[20:32], 12)

            elif s.opcode == STORE:
                # SB, SH, SW
                if funct3 == b'000':  # SB
                    s.imm @= sext(concat(s.instr[7:12], s.instr[25:32]), 12)
                elif funct3 == b'001':  # SH
                    s.imm @= sext(concat(s.instr[7:12], s.instr[25:32]), 12)
                elif funct3 == b'010':  # SW
                    s.imm @= sext(concat(s.instr[7:12], s.instr[25:32]), 12)

            elif s.opcode == BRANCH:
                # BEQ, BNE, BLT, BGE, BLTU, BGEU
                s.imm @= sext(concat(s.instr[31], s.instr[7], s.instr[25:30], s.instr[8:11]), 12)
                if funct3 == b'000':  # BEQ
                    s.alu @= 0b1100  # BEQ
                elif funct3 == b'001':  # BNE
                    s.alu @= 0b1101  # BNE
                elif funct3 == b'100':  # BLT
                    s.alu @= 0b1110  # BLT
                elif funct3 == b'101':  # BGE
                    s.alu @= 0b1111  # BGE
                elif funct3 == b'110':  # BLTU
                    s.alu @= 0b1000  # BLTU
                elif funct3 == b'111':  # BGEU
                    s.alu @= 0b1001  # BGEU

            elif s.opcode == LUI:
                # LUI
                s.imm @= s.instr[12:32]
                s.alu @= 0b1010  # LUI
            elif s.opcode == AUIPC:  ## READ !!!!
                # AUIPC
                s.imm @= s.instr[12:32]
                s.alu @= 0b1011  # AUIPC

            elif s.opcode == JAL:
                # JAL
                s.imm @= sext(concat(s.instr[12], s.instr[20:31], s.instr[12:20], s.instr[31]), 21)
                s.alu @= 0b1100  # JAL

            elif s.opcode == JALR:
                # JALR
                s.imm @= sext(s.instr[20:32], 12)
                s.alu @= 0b1101  # JALR

            elif s.opcode == SYSTEM:
                # Here you can implement SYSTEM instructions like ECALL, EBREAK, etc.
                # The provided code is a simple example and does not cover all the SYSTEM instructions.
                if funct3 == b'000':
                    if s.instr[20:32] == b'000000000000':  # ECALL
                        s.alu @= 0b1110  # ECALL
                    elif s.instr[20:32] == b'000000000001':  # EBREAK
                        s.alu @= 0b1111
