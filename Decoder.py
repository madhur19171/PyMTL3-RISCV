from pymtl3 import *
from IFUnit import IFUnit
from RegisterFile import RegisterFile


class Decoder(Component):

    def __init__(self):
        self.instructionOut = None
        self.destinationReg = None
        self.sourceReg2 = None
        self.opcode = None
        self.sourceReg1 = None
        self.instruction = None

    def construct(self):
        self.instruction = InPort(32)
        self.opcode = OutPort(7)
        self.sourceReg1 = OutPort(5)
        self.sourceReg2 = OutPort(5)
        self.destinationReg = OutPort(5)
        self.instructionOut = OutPort(32)

        @update_ff
        def block():
            self.opcode <<= self.instruction[25:31]
            self.sourceReg1 <<= self.instruction[20:24]
            self.sourceReg2 <<= self.instruction[15:19]
            self.destinationReg <<= self.instruction[10:14]

