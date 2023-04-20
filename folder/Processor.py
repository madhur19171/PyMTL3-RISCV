from pymtl3 import *
from InstructionMemory import InstructionMemory
from IFUnit import IFUnit
from Decoder import Decoder
from Execute import Execute
from MemoryAccess import MemoryAccess
from WriteBack import WriteBack

class Processor(Component):
    def construct(s):
        s.InstructionMemoryEnable = 1
        s.instruction = Wire(32)

        s.InstructionMem = InstructionMemory()
        s.InstructionMem.en //= s.InstructionMemoryEnable
        s.InstructionMem.dataOut //= s.instruction

        s.stall = Wire(1)
        s.address = s.instruction
        s.isBranchTaken = Wire(1)
        s.branchInstructionIn = Wire(1)
        s.en = InPort(1)
        s.instructionOut = OutPort(32)
        s.nextPC = Wire(32)

        s.IFunit =IFUnit()




        s.Decoder = Decoder()



        s.Execute = Execute()



        s.MemoryAccess = MemoryAccess()



        s.WriteBack = WriteBack()

