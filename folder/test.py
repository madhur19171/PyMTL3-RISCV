from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from Decoder import Decoder

model = Decoder()
model.set_metadata(VerilogTranslationPass.enable, True)
model.apply(VerilogTranslationPass())
