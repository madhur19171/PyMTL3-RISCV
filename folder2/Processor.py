from pymtl3 import *
from IFUnit_alter import IFUnit_alter
from Decoder import Decoder
from Execute import Execute
from MemoryAccess import MemoryAccess
from WriteBack import WriteBack

class Processor(Component):
    def construct(s):
        s.stall = Wire(1)
        s.isBranchTaken = Wire(1)
        s.en = 1
        s.branchInstructionIn = Wire(8)
        s.instruction = Wire(32)
        s.instructionAddress = Wire(8)

        s.IFUnit = IFUnit_alter()
        s.IFUnit.en = s.en
        s.IFUnit.stall //= s.stall
        s.IFUnit.isBranchTaken //= s.isBranchTaken

        @update
        def instructionAssign():
            s.instruction @= s.IFUnit.instructionOut
            s.instructionAddress @= s.IFUnit.instructionAddressOut

        s.writeEnable = Wire(1)
        s.func7 = Wire(7)
        s.opcode = Wire(7)
        s.func3 = Wire(3)
        s.immediate = Wire(32)
        s.programCounter = Wire(32)
        s.DecoderDataOutRegister1 = Wire(32)
        s.DecoderDataOutRegister2 = Wire(32)


        s.Decoder = Decoder()
        s.Decoder.instruction //= s.instruction
        s.Decoder.writeEnable // s.writeEnable

        @update
        def DecoderToExecute():
            s.func7 @= s.Decoder.func7
            s.func3 @= s.Decoder.func3
            s.opcode @= s.Decoder.opcode
            s.immediate @= s.Decoder.immediate
            s.programCounter @= s.Decoder.programCounter
            s.DecoderDataOutRegister1 @= s.Decoder.DecoderDataOutSourceRegister1
            s.DecoderDataOutRegister2 @= s.Decoder.DecoderDataOutSourceRegister2

        s.Execute = Execute()



        s.MemoryAccess = MemoryAccess()



        s.WriteBack = WriteBack()

