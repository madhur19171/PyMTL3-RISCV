from pymtl3 import *


class progmem(Component):

    def __init__(self):
        self.dout = None
        self.mem = None
        self.O1 = None
        self.WBM1 = None
        self.I1 = None
        self.ADDR = None
        self.CLK = None

    def construct(self, num_bits=32, num_words=256):

        addr_width = clog2(num_words)  # address width
        dtype = mk_bits(num_bits)  # Defining data type

        self.CLK = InPort(1)  # clk
        self.ADDR = InPort(mk_bits(addr_width))  # address
        self.ADDR_out = OutPort(mk_bits(addr_width))  # address
        self.I1 = InPort(dtype)  # write data
        self.O1 = OutPort(dtype)  # read data
        self.WEN = InPort(1)  # bWrite enable

        # memory array

        self.mem = [Wire(dtype) for x in range(num_words)]

        # read path

        self.dout = Wire(dtype)

        # @update_ff
        # def write_logic():
        #     if s.WEN1 == 1:
        #         for i in range(num_bits):
        #             s.mem[s.ADDR][i] <<= s.I1[i]

        @update_ff
        def read_logic():
            for i in range(num_bits):
                self.dout[i] <<= self.mem[self.ADDR][i]

        @update
        def incr():
            self.ADDR @= self.ADDR + 1
