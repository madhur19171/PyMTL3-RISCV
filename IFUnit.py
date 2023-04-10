from pymtl3 import *


class IFUnit(Component):

    def __init__(self):
        self.nextPC = None
        self.instructionOut = None
        self.en = None
        self.branchInstructionIn = None
        self.isBranchTaken = None
        self.address = None
        self.stall = None

    def construct(self):
        self.stall = InPort(1)
        self.address = InPort(8)
        self.isBranchTaken = InPort(1)
        self.branchInstructionIn = InPort(32)
        self.en = InPort(1)
        self.instructionOut = OutPort(32)
        self.nextPC = Wire(32)

        @update_ff
        def assignPC():
            if self.stall != 1:
                self.instructionOut <<= self.nextPC

        @update
        def choosePC():
            if self.isBranchTaken == 1:
                self.nextPC @= self.branchInstructionIn
            else:
                self.nextPC @= self.instructionOut + 4
