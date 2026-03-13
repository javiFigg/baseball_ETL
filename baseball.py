# The purpose of the following file is to build the backbone of my baseball data project
# Once I am able to create and sort the data I will be slowly improving the structure

from dataclass import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import logging

import pandas as pd
import matplotlib.pyplot as plt


# -------------------- Paths & Logging Config ------------------
BASEPATH = path(__file__).resolve().parent
RAWDATA = BASEPATH / "data" / "chunk_0.csv"
OUTDIR = BASEPATH / "out"
1q