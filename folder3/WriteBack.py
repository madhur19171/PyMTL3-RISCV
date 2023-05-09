from pymtl3 import *
from RegisterFile import RegisterFile
class WriteBack(Component):
    def construct(s):
        s.dataIn = InPort(32)
        s.isBranchInstruction = InPort(1)
        s.AddrDestinationRegister = InPort(5)
        s.isLoadInstruction = InPort(1)
        s.isBranchTaken = InPort(1)
        s.programCounterOut = OutPort(32)

        s.RegisterFile = RegisterFile()
        s.RegisterFile.writeEnable //= s.isLoadInstruction
        s.RegisterFile.readEnable //= 0
        s.RegisterFile.AddrSourceRegister2 //= 0
        s.RegisterFile.AddrSourceRegister1 //= 0
        s.RegisterFile.AddrDestinationRegister //= s.AddrDestinationRegister
        s.RegisterFile.dataIn //= s.dataIn

        s.LocalVal1 = Wire(32)
        s.LocalVal2 = Wire(32)

        @update
        def programUpdate():
            if s.isBranchInstruction == 1:
                s.programCounterOut @= s.dataIn
        @update
        def RegFile():
            s.RegisterFile.dataOutSourceRegister1 @= s.LocalVal1
            s.RegisterFile.dataOutSourceRegister2 @= s.LocalVal2





