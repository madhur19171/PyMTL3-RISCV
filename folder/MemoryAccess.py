from pymtl3 import *
from MainMemory import MainsMemory

class MemoryAccess(Component):
    def connect(s):
        s.result = InPort(32)
        s.memoryAddress = InPort(32)
        s.isLoadInstruction = InPort(1)
        s.isStoreInstruction = InPort(1)
        s.memoryData = InPort(32)
        s.branch = InPort(32)
        s.jumpAddress = InPort(32)
        s.isBranchTaken = InPort(1)

        s.dataOut = OutPort(32)

        s.MainsMemory = MainsMemory()
        if s.isLoadInstruction == 1:
            s.MainsMemory.readEnable //= 1  # Request
        if s.isStoreInstruction == 1:
            s.MainsMemory.strobe //= 1111
            s.MainsMemory.writeEnable //=1
        else:
            s.MainsMemory.writeEnable //= 0  # Write enable
            s.MainsMemory.readEnable //= 0  # Request
        #s.MainsMemory.strobe //= 0000
        s.MainsMemory.address //= s.memoryAddress  # address
        s.MainsMemory.dataIn //= s.result  # write data
        s.MainsMemory.dataOut //= s.dataOut  # read data, Instruction stored in the instruction memory.


