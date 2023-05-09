from pymtl3 import *
import numpy as np

class Execute(Component):

    def construct(s):

        # InPorts
        #s.instruction = InPort(32)
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
                    s.result @= s.dataSourceRegister1 + immediate
                elif funct3 == 0b010:  # SLTI
                    s.result @= 1 if(s.dataSourceRegister1 < immediate) else 0
                # elif funct3 == 0b011:  # SLTIU
                #     s.result @= (abs(s.dataSourceRegister1) < abs(immediate))
                elif funct3 == 0b100:  # XORI
                    s.result @= s.dataSourceRegister1 ^ immediate
                elif funct3 == 0b110:  # ORI
                    s.result @= s.dataSourceRegister1 | immediate
                elif funct3 == 0b111:  # ANDI
                    s.result @= s.dataSourceRegister1 & immediate
                elif (funct3 == 0b001) & (funct7 == 0b0000000):  # SLLI
                    s.result @= s.dataSourceRegister1 << immediate[0:5]
                elif funct3 == 0b101:
                    if funct7 == 0b0000000:  # SRLI
                        s.result @= s.dataSourceRegister1 >> immediate[0:5]
                    elif funct7 == 0b0100000:  # SRAI
                        s.result @= s.dataSourceRegister1 >> immediate[0:5]

            # OP instructions
            elif opcode == 0b0110011:
                if funct3 == 0b000:
                    if funct7 == 0b0000000:  # ADD
                        s.result @= s.dataSourceRegister1 + s.dataSourceRegister2
                    elif funct7 == 0b0100000:  # SUB
                        s.result @= s.dataSourceRegister1 - s.dataSourceRegister2
                elif (funct3 == 0b001) & (funct7 == 0b0000000):  # SLL
                    s.result @= s.dataSourceRegister1 << s.dataSourceRegister2[0:5]
                elif funct3 == 0b010:  # SLT
                    s.result @= 1 if(s.dataSourceRegister1 < s.dataSourceRegister2) else 0
                elif funct3 == 0b011:  # SLTU
                    s.result @= 1 if(s.dataSourceRegister1 < s.dataSourceRegister2) else 0
                elif funct3 == 0b100:  # XOR
                    s.result @= s.dataSourceRegister1 ^ s.dataSourceRegister2
                elif funct3 == 0b101:
                    if funct7 == 0b0000000:  # SRL
                        s.result @= s.dataSourceRegister1 >> s.dataSourceRegister2[0:5]
                    elif funct7 == 0b0100000:  # SRA
                        s.result @= s.dataSourceRegister1 >> s.dataSourceRegister2[0:5]
                elif funct3 == 0b110:  # OR
                    s.result @= s.dataSourceRegister1 | s.dataSourceRegister2
                elif funct3 == 0b111:  # AND
                    s.result @= s.dataSourceRegister1 & s.dataSourceRegister2

            # Load instructions
            elif opcode == 0b0000011:
                s.isLoadInstruction @= 1
                if funct3 == 0b000:  # LB
                    s.memoryAddress @= s.dataSourceRegister1 + immediate
                    s.result @= s.memoryAddress
                elif funct3 == 0b001:  # LH
                    s.memoryAddress @= s.dataSourceRegister1 + immediate
                    s.result @= s.memoryAddress
                elif funct3 == 0b010:  # LW
                    s.memoryAddress @= s.dataSourceRegister1 + immediate
                    s.result @= s.memoryAddress

            # Store instructions
            elif opcode == 0b0100011:
                s.isStoreInstruction @= 1
                if funct3 == 0b000:  # SB
                    s.memoryAddress @= s.dataSourceRegister1 + immediate
                elif funct3 == 0b001:  # SH
                    s.memoryAddress @= s.dataSourceRegister1 + immediate
                elif funct3 == 0b010:  # SW
                    s.memoryAddress @= s.dataSourceRegister1 + immediate

            # result instructions
            elif opcode == 0b1100011:
                s.isBranchTaken @= 1
                if funct3 == 0b000:  # BEQ
                    if s.dataSourceRegister1 == s.dataSourceRegister2:
                        s.result @= s.programCounter + immediate
                elif funct3 == 0b001:  # BNE
                    if s.dataSourceRegister1 != s.dataSourceRegister2:
                        s.result @= s.programCounter + immediate
                elif funct3 == 0b100:  # BLT
                    if s.dataSourceRegister1 < s.dataSourceRegister2:
                        s.result @= s.programCounter + immediate
                elif funct3 == 0b101:  # BGE
                    if s.dataSourceRegister1 >= s.dataSourceRegister2:
                        s.result @= s.programCounter + immediate
                elif funct3 == 0b110:  # BLTU
                    if s.dataSourceRegister1 < s.dataSourceRegister2:
                        s.result @= s.programCounter + immediate
                elif funct3 == 0b111:  # BGEU
                    if s.dataSourceRegister1 >= s.dataSourceRegister2:
                        s.result @= s.programCounter + immediate

            # Jump instructions
            elif opcode == 0b1101111:  # JAL
                s.result @= s.programCounter + immediate

            elif opcode == 0b1100111:  # JALR
                s.result @= (s.dataSourceRegister1 + immediate) & (0xFFFFFFFE)

