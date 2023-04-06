from pymtl3 import *
from Memory import Memory
from RegisterFile import RegisterFile
from IFUnit import IFUnit
from Decoder import Decoder
class Processor(Component):
    def construct(self):
        self.enInstructionMemory = 1
        self.