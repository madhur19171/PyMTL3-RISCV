from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from Processor import Processor
from Decoder import Decoder
from Execute import Execute
from IFUnit_alter import IFUnit_alter
from InstructionMemory import InstructionMemory
from MainMemory import MainsMemory
from MemoryAccess import MemoryAccess
from RegisterFile import RegisterFile
from WriteBack import WriteBack


# # -------------------------------------------------------------------------
# # Processor Test
# # -------------------------------------------------------------------------
#
# def test_Processor(cmdline_opts):
#     run_test_vector_sim(Processor(), [
#         (
#             'writeEnable readEnable AddrSourceRegister1 AddrSourceRegister2 AddrDestinationRegister dataIn dataOutSourceRegister1* dataOutSourceRegister2*'),
#         [0x00, '?'],
#         [0x03, 0x01],
#         [0x06, 0x04],
#         [0x00, 0x07],
#     ], cmdline_opts)


# -------------------------------------------------------------------------
# Register Test
# -------------------------------------------------------------------------

def test_register(cmdline_opts):
    run_test_vector_sim(RegisterFile(), [
        (
            'writeEnable readEnable AddrSourceRegister1 AddrSourceRegister2 AddrDestinationRegister dataIn dataOutSourceRegister1* dataOutSourceRegister2*'),
        [0x00, '?'],
        [0x03, 0x01],
        [0x06, 0x04],
        [0x00, 0x07],
    ], cmdline_opts)


# -------------------------------------------------------------------------
# WriteBack Test
# -------------------------------------------------------------------------
def test_writeback(cmdline_opts):
    run_test_vector_sim(WriteBack(), [
        (
            'dataIn  isBranchInstruction AddrDestinationRegister isLoadInstruction isBranchTaken writeEnable* programCounterOut*'),
        [0x00, '?'],
        [0x03, 0x01],
        [0x06, 0x04],
        [0x00, 0x07],
    ], cmdline_opts)


# -------------------------------------------------------------------------
# Memory Access Test
# -------------------------------------------------------------------------
def test_memoryAccess(cmdline_opts):
    run_test_vector_sim(MemoryAccess(), [
        (
            'result memoryAddress isLoadInstruction isStoreInstruction memoryData branch jumpAddress isBranchTaken dataOut*'),
        [0x00, '?'],
        [0x03, 0x01],
        [0x06, 0x04],
        [0x00, 0x07],
    ], cmdline_opts)


# -------------------------------------------------------------------------
# IF Unit Test
# -------------------------------------------------------------------------
def test_IFUNIT(cmdline_opts):
    run_test_vector_sim(IFUnit_alter(), [
        (
            'stall isBranchTaken branchInstructionIn en instructionOut* instructionAddressOut*'),
        [0x00, '?'],
        [0x03, 0x01],
        [0x06, 0x04],
        [0x00, 0x07],
    ], cmdline_opts)


# -------------------------------------------------------------------------
# Main Memory Test
# -------------------------------------------------------------------------
def test_mainmemory(cmdline_opts):
    run_test_vector_sim(MainsMemory(), [
        (
            'readEnable writeEnable strobe address dataIn dataOut*'),
        [0x00, '?'],
        [0x03, 0x01],
        [0x06, 0x04],
        [0x00, 0x07],
    ], cmdline_opts)

# -------------------------------------------------------------------------
# Decoder Test
# -------------------------------------------------------------------------
def test_decoder(cmdline_opts):
    run_test_vector_sim(Decoder(), [
        (
            'writeEnable instruction func7* opcode* func3* immediate* programCounter* DecoderDataOutSourceRegister1* DecoderDataOutSourceRegister2*'),
        [0x00, '?'],
        [0x03, 0x01],
        [0x06, 0x04],
        [0x00, 0x07],
    ], cmdline_opts)

# -------------------------------------------------------------------------
# Execute Test
# -------------------------------------------------------------------------
def test_execute(cmdline_opts):
    run_test_vector_sim(Execute(), [
        (
            'instruction dataSourceRegister1 dataSourceRegister2 immediate programCounter func7 func3 opcode result* memoryAddress* isLoadInstruction* isStoreInstruction* memoryData* branch* jumpAddress* isBranchTaken*'),
        [0x00, '?'],
        [0x03, 0x01],
        [0x06, 0x04],
        [0x00, 0x07],
    ], cmdline_opts)

# -------------------------------------------------------------------------
# InstructionMemory Test
# -------------------------------------------------------------------------
def test_InstructionMemory(cmdline_opts):
    run_test_vector_sim(InstructionMemory(), [
        (
            'en address dataOut*'),
        [0x00, '?'],
        [0x03, 0x01],
        [0x06, 0x04],
        [0x00, 0x07],
    ], cmdline_opts)
