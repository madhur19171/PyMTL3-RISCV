from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from Processor import Processor

model = Processor()
model.set_metadata(VerilogTranslationPass.enable, True)
model.apply(VerilogTranslationPass())
