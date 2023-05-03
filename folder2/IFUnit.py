from pymtl3 import *
from InstructionMemory import InstructionMemory

class IFUnit(Component):

    def __init__(s):
        s.nextPC = None
        s.instructionOut = None
        s.en = None
        s.branchInstructionIn = None
        s.isBranchTaken = None
        s.address = None
        s.stall = None

    def construct(s):
        s.stall = InPort(1)
        s.address = InPort(8)
        s.isBranchTaken = InPort(1)
        s.branchInstructionIn = InPort(32)
        s.en = InPort(1)
        s.instructionOut = OutPort(32)
        s.nextPC = Wire(32)

        s.InstructionMemory  = InstructionMemory()
        s.InstructionMemory.en = s.en
        s.InstructionMemory.address = s.address

        @update_ff
        def assignPC():
            if s.en ==1 and s.stall != 1:
                s.instructionOut <<= s.nextPC

        @update
        def choosePC():
            if s.isBranchTaken == 1:
                s.nextPC @= s.branchInstructionIn
            else:
                s.nextPC @= s.instructionOut + 4
