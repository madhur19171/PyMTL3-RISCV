from pymtl3 import *
from DataMemory import DataMemory
from RegisterFile import RegisterFile
from IFUnit import IFUnit
from RISCVDecoder import RISCVDecoder
from Execute import ExecuteUnit
from InstructionMemory import InsMemory

class Processor(Component):

    def __init__(self):
        pass

    def construct(self):

        self.IF_Unit = IFUnit()
        self.Data_Memory = DataMemory()
        self.Register_File = RegisterFile()
        self.Decoder = RISCVDecoder()
        self.Execute = ExecuteUnit()
        self.Ins_Memory = InsMemory()

        # Fetch Instruction
        self.stall = Wire(1)
        self.address = Wire(8)
        self.isBranchTaken = Wire(1)
        self.branchInstructionIn = Wire(32)
        self.en = Wire(1)
        self.instructionOut = Wire(32)
        self.nextPC = Wire(32)

        self.stall //= self.IF_Unit.stall
        self.address //= self.IF_Unit.address
        self.isBranchTaken //= self.IF_Unit.isBranchTaken
        self.branchInstructionIn //= self.IF_Unit.branchInstructionIn
        self.en //= self.IF_Unit.en
        self.instructionOut //= self.IF_Unit.instructionOut
        self.nextPC //= self.IF_Unit.nextPC

        # Pipeline State Update
        @update_ff
        def PiplineUpdate():
            # FETCH -> DECODE
            self.Decoder.instr <<= self.instructionOut

            # DECODE -> EXECUTE
            self.Execute.instr <<= self.Decoder.PC
            self.Execute.rs1 <<= self.Decoder.rs1
            self.Execute.rs2 <<= self.Decoder.rs2
            self.Execute.imm <<= self.Decoder.immediate
            self.Execute.pc <<= self.Decoder.PC
            self.Execute.func7 <<= self.Decoder.funct7
            self.Execute.func3 <<= self.Decoder.funct3
            self.Execute.opcode <<= self.Decoder.opcode











