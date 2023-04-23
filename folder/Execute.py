from pymtl3 import *
import numpy as np

class Execute(Component):

    def construct(s):

        # InPorts
        s.instruction = InPort(32)
        s.dataSourceRegister1 = InPort(32)
        s.dataSourceRegister2 = InPort(32)
        s.immediate = InPort(32)
        s.programCounter = InPort(32)
        s.func7 = InPort(7)
        s.func3 = InPort(3)
        s.opcode = InPort(7)

        # OutPorts
        s.result = OutPort(32)
        s.memoryAddress = OutPort(32)
        s.isLoadInstruction = OutPort(1)
        s.isStoreInstruction = OutPort(1)
        s.memoryData = OutPort(32)
        s.branch = OutPort(32)
        s.jumpAddress = OutPort(32)
        s.isBranchTaken = OutPort(1)

        @update
        def execute():
            opcode = s.opcode
            funct3 = s.func3
            funct7 = s.func7
            immediate = s.immediate

            # OP_IMM instructions
            if opcode == 0b0010011:
                if funct3 == 0b000:  # ADDI
                    s.result = s.dataSourceRegister1 + immediate
                elif funct3 == 0b010:  # SLTI
                    s.result = (int(s.dataSourceRegister1 < immediate))
                elif funct3 == 0b011:  # SLTIU
                    s.result = (int(np.uint(s.dataSourceRegister1) < np.uint(immediate)))
                elif funct3 == 0b100:  # XORI
                    s.result = s.dataSourceRegister1 ^ immediate
                elif funct3 == 0b110:  # ORI
                    s.result = s.dataSourceRegister1 | immediate
                elif funct3 == 0b111:  # ANDI
                    s.result = s.dataSourceRegister1 & immediate
                elif funct3 == 0b001 and funct7 == 0b0000000:  # SLLI
                    s.result = s.dataSourceRegister1 << immediate[0:5]
                elif funct3 == 0b101:
                    if funct7 == 0b0000000:  # SRLI
                        s.result = s.dataSourceRegister1 >> immediate[0:5]
                    elif funct7 == 0b0100000:  # SRAI
                        s.result = s.dataSourceRegister1 >> immediate[0:5]

            # OP instructions
            elif opcode == 0b0110011:
                if funct3 == 0b000:
                    if funct7 == 0b0000000:  # ADD
                        s.result = s.dataSourceRegister1 + s.dataSourceRegister2
                    elif funct7 == 0b0100000:  # SUB
                        s.result = s.dataSourceRegister1 - s.dataSourceRegister2
                elif funct3 == 0b001 and funct7 == 0b0000000:  # SLL
                    s.result = s.dataSourceRegister1 << s.dataSourceRegister2[0:5]
                elif funct3 == 0b010:  # SLT
                    s.result = (int(s.dataSourceRegister1 < s.dataSourceRegister2))
                elif funct3 == 0b011:  # SLTU
                    s.result = (int(np.uint(s.dataSourceRegister1) < np.uint(s.dataSourceRegister2)))
                elif funct3 == 0b100:  # XOR
                    s.result = s.dataSourceRegister1 ^ s.dataSourceRegister2
                elif funct3 == 0b101:
                    if funct7 == 0b0000000:  # SRL
                        s.result = s.dataSourceRegister1 >> s
                        s.result = s.dataSourceRegister1 >> s.dataSourceRegister2[0:5]
                    elif funct7 == 0b0100000:  # SRA
                        s.result = s.dataSourceRegister1 >> s.dataSourceRegister2[0:5]
                elif funct3 == 0b110:  # OR
                    s.result = s.dataSourceRegister1 | s.dataSourceRegister2
                elif funct3 == 0b111:  # AND
                    s.result = s.dataSourceRegister1 & s.dataSourceRegister2

            # Load instructions
            elif opcode == 0b0000011:
                s.isLoadInstruction = 1
                if funct3 == 0b000:  # LB
                    s.memoryAddress = s.dataSourceRegister1 + immediate
                    #s.memoryData = s.mem[s.memoryAddress][0:8].sext(32)
                    s.result = s.memoryAddress
                elif funct3 == 0b001:  # LH
                    s.memoryAddress = s.dataSourceRegister1 + immediate
                    #s.memoryData = s.mem[s.memoryAddress][0:16].sext(32)
                    s.result = s.memoryAddress
                elif funct3 == 0b010:  # LW
                    s.memoryAddress = s.dataSourceRegister1 + immediate
                    #s.memoryData = s.mem[s.memoryAddress].sext(32)
                    s.result = s.memoryAddress

            # Store instructions
            elif opcode == 0b0100011:
                s.isStoreInstruction = 1
                if funct3 == 0b000:  # SB
                    s.memoryAddress = s.dataSourceRegister1 + immediate
                    s.memoryData = s.dataSourceRegister2[0:8]
                    # s.mem[s.memoryAddress][0:8] = s.memoryData[0:8]
                elif funct3 == 0b001:  # SH
                    s.memoryAddress = s.dataSourceRegister1 + immediate
                    s.memoryData = s.dataSourceRegister2[0:16]
                    # s.mem[s.memoryAddress][0:16] = s.memoryData[0:16]
                elif funct3 == 0b010:  # SW
                    s.memoryAddress = s.dataSourceRegister1 + immediate
                    s.memoryData = s.dataSourceRegister2
                    # s.mem[s.memoryAddress] = s.memoryData

            # Branch instructions
            elif opcode == 0b1100011:
                s.isBranchTaken = 1
                if funct3 == 0b000:  # BEQ
                    if s.dataSourceRegister1 == s.dataSourceRegister2:
                        s.branch = s.pc + immediate
                elif funct3 == 0b001:  # BNE
                    if s.dataSourceRegister1 != s.dataSourceRegister2:
                        s.branch = s.pc + immediate
                elif funct3 == 0b100:  # BLT
                    if s.dataSourceRegister1 < s.dataSourceRegister2:
                        s.branch = s.pc + immediate
                elif funct3 == 0b101:  # BGE
                    if s.dataSourceRegister1 >= s.dataSourceRegister2:
                        s.branch = s.pc + immediate
                elif funct3 == 0b110:  # BLTU
                    if np.uint(s.dataSourceRegister1) < np.uint(s.dataSourceRegister2):
                        s.branch = s.pc + immediate
                elif funct3 == 0b111:  # BGEU
                    if np.uint(s.dataSourceRegister1) >= np.uint(s.dataSourceRegister2):
                        s.branch = s.pc + immediate

            # Jump instructions
            elif opcode == 0b1101111:  # JAL
                s.jumpAddress = s.pc + immediate
                s.result = s.pc + 4

            elif opcode == 0b1101111:  # JAL
                s.jumpAddress = s.pc + immediate
                s.result = s.pc + 4

            elif opcode == 0b1100111:  # JALR
                s.jumpAddress = (s.dataSourceRegister1 + immediate) & (0xFFFFFFFE)
                s.result = s.pc + 4

            # Fence instruction
            elif opcode == 0b0001111 and funct3 == 0b000 and immediate == 0b000000000000:  # FENCE
                pass  # Do nothing for now

            # System instructions
            elif opcode == 0b1110011:
                if funct3 == 0b000 and immediate == 0b000000000000:  # ECALL
                    pass  # Do nothing for now
                elif funct3 == 0b000 and immediate == 0b000000000001:  # EBREAK
                    pass  # Do nothing for now

            # Unrecognized instruction

        def line_trace(s):
            return f"pc = {s.pc:x} instruction = {s.instruction:x} result = {s.result:x}"