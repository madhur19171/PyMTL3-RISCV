from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from Memory import Memory

model = Memory()
model.set_metadata(VerilogTranslationPass.enable, True)
model.apply(VerilogTranslationPass())
