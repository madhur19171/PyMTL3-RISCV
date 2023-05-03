from pymtl3 import *

class MainsMemory(Component):

    def construct(self):
        strobeWidth = 4
        strobType = mk_bits(strobeWidth)

        self.readEnable = InPort(1)  # Request
        self.writeEnable = InPort(1)  # Write enable
        self.strobe = InPort(strobType)
        self.address = InPort(32)  # address
        self.dataIn = InPort(32)  # write data
        self.dataOut = OutPort(32)  # read data, Instruction stored in the instruction memory.
        # memory array
        self.mem = [Wire(32) for x in range(256)]

        @update_ff
        def read_logic():
            if (self.readEnable == 1) & (self.writeEnable != 1):
                self.dataOut <<= self.mem[self.address[0:8]]

        @update_ff
        def write_logic():
            if (self.readEnable == 1) & (self.writeEnable == 1):
                for i in range(strobeWidth):
                    if self.strobe[i] == 1:
                        a = 8 * i
                        for j in range(8):
                            self.mem[self.address[0:8]][a + j] <<= self.dataIn[a + j]


