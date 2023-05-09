from pymtl3 import *
from InstructionMemory import InstructionMemory


class IFUnit_alter(Component):

    def construct(s):
        s.stall                     = InPort(1)
        s.isBranchTaken             = InPort(1)
        s.branchInstructionIn       = InPort(8)
        s.en                        = InPort(1)
        s.instructionOut            = OutPort(32)
        s.instructionAddressOut     = OutPort(8)
        s.nextPC                    = Wire(8)

        s.instructionMemory = InstructionMemory()
        s.instructionMemory.en //= s.en

        s.tempAddressMem = Wire(8)
        s.tempAddress = Wire(8)
        @update
        def sendAddress():
            if (s.en == 1) & (s.stall != 1):
                if s.isBranchTaken == 1:
                    s.instructionMemory.address  @= s.branchInstructionIn
                else:
                    s.instructionMemory.address  @= s.nextPC
                    s.nextPC @= s.tempAddress + 4
            else:
                s.instructionAddressOut @= 0
            s.instructionAddressOut @= s.instructionMemory.address

        @update
        def assignData():
            if s.stall == 1:
                s.instructionOut @= 0
            else:
                s.instructionOut @= s.instructionMemory.dataOut

        @update_ff
        def Assign():
            s.tempAddress <<= s.nextPC