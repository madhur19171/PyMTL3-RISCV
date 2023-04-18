from pymtl3 import *


class RegisterFile(Component):

    def __init__(self):
        self.RegisterFile = None
        self.dataOutSourceRegister2 = None
        self.dataOutSourceRegister1 = None
        self.dataIn = None
        self.AddrDestinationRegister = None
        self.AddrSourceRegister2 = None
        self.AddrSourceRegister1 = None
        self.ren = None
        self.wen = None
        # self.clk = None

    def construct(self):
        # self.clk = InPort(1)

        # InPort
        self.wen = InPort(1)
        self.ren = InPort(1)
        self.AddrSourceRegister1 = InPort(5)
        self.AddrSourceRegister2 = InPort(5)
        self.AddrDestinationRegister = InPort(5)
        self.dataIn = InPort(32)

        # OutPort
        self.dataOutSourceRegister1 = OutPort(32)
        self.dataOutSourceRegister2 = OutPort(32)
        
        self.RegisterFile = [Wire(32) for i in range(32)]
    
        @update
        def read_register_file():
            if self.ren == 1:
                self.dataOutSourceRegister1 @= self.RegisterFile[self.AddrSourceRegister1]
                self.dataOutSourceRegister2 @= self.RegisterFile[self.AddrSourceRegister2]
        
        @update
        def write_back():
            if self.wen == 1:
                self.RegisterFile[self.AddrDestinationRegister] @= self.dataIn
        

                
