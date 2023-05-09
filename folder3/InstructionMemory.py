from pymtl3 import *


class InstructionMemory(Component):

    def construct(self):
        self.en = InPort(1)  # Request
        self.address = InPort(8)  # address
        self.dataOut = OutPort(32)  # read instruction, stored in the instruction memory.
        self.mem = [Wire(32) for x in range(256)]

        @update_ff
        def read_logic():
            if self.en == 1:
                self.dataOut <<= self.mem[self.address]

