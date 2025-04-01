name = "StellarInfra"
from . import DirManage as siDM
from . import IO as siIO
from .Logger import CLog
#StageControl

#IO

#CLog

#CDirectoryConfig

try:
    import numpy as np
except:
    np = None
try:
    from matplotlib import pyplot as plt
except:
    plt = None
import os
from pathlib import Path