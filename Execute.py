from pymtl3 import *
import numpy as np
#from RegisterFile import RegisterFile

class Bits32:
    def __int__(self):
        return mk_bits(32)


class Bits1:
    def __int__(self):
        return mk_bits(1)


class ExecuteUnit(Component):


    def __init__(self):
        self.instr = None

    def construct(s):

        # InPorts
        s.instr = InPort(Bits32)
        s.rs1 = InPort(Bits32)
        s.rs2 = InPort(Bits32)
        s.rd = InPort(Bits32)
        s.imm = InPort(Bits32)
        s.pc = InPort(Bits32)
        s.func7 = InPort(7)
        s.func3 = InPort(3)
        s.opcode = InPort(7)

        # OutPorts
        s.result = OutPort(Bits32)
        s.mem_addr = OutPort(Bits32)
        s.mem_data = OutPort(Bits32)
        s.branch = OutPort(Bits32)
        s.jump_addr = OutPort(Bits32)


        # # Wire
        # s.wen = Wire(1)
        # s.ren = Wire(1)
        # s.dataSourceRegister1 = Wire(32)
        # s.dataSourceRegister2 = Wire(32)
        # # Memory Instance
        # s.mem = RegisterFile()
        # s.mem.wen //= s.wen
        # s.mem.ren //= 1
        # s.mem.AddrSourceRegister1 //= s.rs1
        # s.mem.AddrSourceRegister2 //= s.rs2
        # s.mem.AddrDestinationRegister //= s.result
        # s.mem.dataIn //= 0
        # s.mem.dataOutSourceRegister1 //= s.dataSourceRegister1
        # s.mem.dataOutSourceRegister2 //= s.dataSourceRegister2
        #

        @update
        def execute():
            opcode = s.opcode
            funct3 = s.func3
            funct7 = s.func7
            imm = s.imm.sext(32)

            # OP_IMM instructions
            if opcode == 0b0010011:
                if funct3 == 0b000:  # ADDI
                    s.result = s.rs1 + imm
                elif funct3 == 0b010:  # SLTI
                    s.result = Bits1(int(s.rs1 < imm))
                elif funct3 == 0b011:  # SLTIU
                    s.result = Bits1(int(np.uint(s.rs1) < np.uint(imm)))
                elif funct3 == 0b100:  # XORI
                    s.result = s.rs1 ^ imm
                elif funct3 == 0b110:  # ORI
                    s.result = s.rs1 | imm
                elif funct3 == 0b111:  # ANDI
                    s.result = s.rs1 & imm
                elif funct3 == 0b001 and funct7 == 0b0000000:  # SLLI
                    s.result = s.rs1 << imm[0:5]
                elif funct3 == 0b101:
                    if funct7 == 0b0000000:  # SRLI
                        s.result = s.rs1 >> imm[0:5]
                    elif funct7 == 0b0100000:  # SRAI
                        s.result = s.rs1 >> imm[0:5]

            # OP instructions
            elif opcode == 0b0110011:
                if funct3 == 0b000:
                    if funct7 == 0b0000000:  # ADD
                        s.result = s.rs1 + s.rs2
                    elif funct7 == 0b0100000:  # SUB
                        s.result = s.rs1 - s.rs2
                elif funct3 == 0b001 and funct7 == 0b0000000:  # SLL
                    s.result = s.rs1 << s.rs2[0:5]
                elif funct3 == 0b010:  # SLT
                    s.result = Bits1(int(s.rs1 < s.rs2))
                elif funct3 == 0b011:  # SLTU
                    s.result = Bits1(int(np.uint(s.rs1) < np.uint(s.rs2)))
                elif funct3 == 0b100:  # XOR
                    s.result = s.rs1 ^ s.rs2
                elif funct3 == 0b101:
                    if funct7 == 0b0000000:  # SRL
                        s.result = s.rs1 >> s
                        s.result = s.rs1 >> s.rs2[0:5]
                    elif funct7 == 0b0100000:  # SRA
                        s.result = s.rs1 >> s.rs2[0:5]
                elif funct3 == 0b110:  # OR
                    s.result = s.rs1 | s.rs2
                elif funct3 == 0b111:  # AND
                    s.result = s.rs1 & s.rs2

            # Load instructions
            elif opcode == 0b0000011:
                if funct3 == 0b000:  # LB
                    s.mem_addr = s.rs1 + imm
                    s.mem_data = s.mem[s.mem_addr][0:8].sext(32)
                    s.result = s.mem_data
                elif funct3 == 0b001:  # LH
                    s.mem_addr = s.rs1 + imm
                    s.mem_data = s.mem[s.mem_addr][0:16].sext(32)
                    s.result = s.mem_data
                elif funct3 == 0b010:  # LW
                    s.mem_addr = s.rs1 + imm
                    s.mem_data = s.mem[s.mem_addr].sext(32)
                    s.result = s.mem_data

            # Store instructions
            elif opcode == 0b0100011:
                if funct3 == 0b000:  # SB
                    s.mem_addr = s.rs1 + imm
                    s.mem_data = s.rs2[0:8].zext(32)
                    s.mem[s.mem_addr][0:8] = s.mem_data[0:8]
                elif funct3 == 0b001:  # SH
                    s.mem_addr = s.rs1 + imm
                    s.mem_data = s.rs2[0:16].zext(32)
                    s.mem[s.mem_addr][0:16] = s.mem_data[0:16]
                elif funct3 == 0b010:  # SW
                    s.mem_addr = s.rs1 + imm
                    s.mem_data = s.rs2.zext(32)
                    s.mem[s.mem_addr] = s.mem_data

            # Branch instructions
            elif opcode == 0b1100011:
                if funct3 == 0b000:  # BEQ
                    if s.rs1 == s.rs2:
                        s.branch = s.pc + imm
                elif funct3 == 0b001:  # BNE
                    if s.rs1 != s.rs2:
                        s.branch = s.pc + imm
                elif funct3 == 0b100:  # BLT
                    if s.rs1 < s.rs2:
                        s.branch = s.pc + imm
                elif funct3 == 0b101:  # BGE
                    if s.rs1 >= s.rs2:
                        s.branch = s.pc + imm
                elif funct3 == 0b110:  # BLTU
                    if np.uint(s.rs1) < np.uint(s.rs2):
                        s.branch = s.pc + imm
                elif funct3 == 0b111:  # BGEU
                    if np.uint(s.rs1) >= np.uint(s.rs2):
                        s.branch = s.pc + imm

            # Jump instructions
            elif opcode == 0b1101111:  # JAL
                s.jump_addr = s.pc + imm
                s.result = s.pc + 4

            elif opcode == 0b1101111:  # JAL
                s.jump_addr = s.pc + imm
                s.result = s.pc + 4

            elif opcode == 0b1100111:  # JALR
                s.jump_addr = (s.rs1 + imm) & Bits32(0xFFFFFFFE)
                s.result = s.pc + 4

            # Fence instruction
            elif opcode == 0b0001111 and funct3 == 0b000 and imm == 0b000000000000:  # FENCE
                pass  # Do nothing for now

            # System instructions
            elif opcode == 0b1110011:
                if funct3 == 0b000 and imm == 0b000000000000:  # ECALL
                    pass  # Do nothing for now
                elif funct3 == 0b000 and imm == 0b000000000001:  # EBREAK
                    pass  # Do nothing for now

            # Unrecognized instruction

        def line_trace(s):
            return f"pc = {s.pc:x} instr = {s.instr:x} result = {s.result:x}"
