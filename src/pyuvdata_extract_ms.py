import os
from pyuvdata import UVData



UV = UVData()

UV.read_mir("../data/raw/201006_14_32_20", receivers='240', sidebands='u', corrchunk=[5])

UV.write_ms("../data/raw/s255irOct_240_u_5.ms")
