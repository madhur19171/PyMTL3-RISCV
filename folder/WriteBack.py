from pymtl3 import *

class WriteBack(Component):
    def construct(s):
        s.dataIn = InPort(32)
        s.isBranchInstruction = InPort(1)
        s.AddrDestinationRegister = InPort(5)
        s.isLoadInstruction = InPort(1)
        s.isBranchTaken = InPort(1)
        s.writeEnable = OutPort(1)
        s.programCounterOut = OutPort(32)
        @update
        def write():
            if s.isSLoadInstruction == 1:
                 s.writeEnable @= 1
        @update
        def programUpdate():
            if s.isBranchInstruction == 1:
                s.programCounterOut @= s.dataIn



