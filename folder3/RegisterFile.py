from pymtl3 import *
class RegisterFile(Component):

    def __init__(self):
        self.dataOutSourceRegister2 = None
        self.dataOutSourceRegister1 = None
        self.dataIn = None
        self.AddrDestinationRegister = None
        self.AddrSourceRegister2 = None
        self.AddrSourceRegister1 = None
        self.readEnable = None
        self.writeEnable = None

    def construct(self):
        self.writeEnable = InPort(1)
        self.readEnable = InPort(1)
        self.AddrSourceRegister1 = InPort(5)
        self.AddrSourceRegister2 = InPort(5)
        self.AddrDestinationRegister = InPort(5)
        self.dataIn = InPort(32)
        self.dataOutSourceRegister1 = OutPort(32)
        self.dataOutSourceRegister2 = OutPort(32)

        self.RegisterFile = [Wire(32) for i in range(32)]

        if self.readEnable == 1 and self.writeEnable !=1:
            @update
            def read_register_file():
                self.dataOutSourceRegister1 <<= self.RegisterFile[self.AddrSourceRegister1]
                self.dataOutSourceRegister2 <<= self.RegisterFile[self.AddrSourceRegister2]

        if self.writeEnable == 1:
            @update
            def write_back():
                if self.writeEnable == 1:
                    self.RegisterFile[self.AddrDestinationRegister] <<= self.dataIn



