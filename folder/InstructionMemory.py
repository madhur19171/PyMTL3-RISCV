from pymtl3 import *


class InstructionMemory(Component):

    def construct(self, dataWidth=32, entries=256):
        addressWidth = clog2(entries)  # address width
        addressType = mk_bits(addressWidth)  # Defining address type
        dataType = mk_bits(dataWidth)  # Defining data type
        strobeWidth = dataWidth // 8
        strobType = mk_bits(strobeWidth)

        self.en = InPort(1)  # Request
        # self.wen = InPort(1)  # Write enable
        # self.strobe = InPort(strobType)
        self.address = InPort(addressType)  # address
        # self.dataIn = InPort(dataType)  # write data
        self.dataOut = OutPort(dataType)  # read instruction, stored in the instruction memory.
        # memory array
        self.mem = [Wire(dataType) for x in range(entries)]

        @update_ff
        def read_logic():
            if self.en == 1:
                self.dataOut <<= self.mem[self.address]

        # @update_ff
        # def write_logic():
        #     if (self.en == 1) & (self.wen == 1):
        #         for i in range(strobeWidth):
        #             if self.strobe[i] == 1:
        #                 a = 8 * i
        #                 for j in range(8):
        #                     self.mem[self.address][a + j] <<= self.dataIn[a + j]
        #
