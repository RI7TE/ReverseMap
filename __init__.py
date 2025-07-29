import sys

from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from ReverseMap.convert import Convertible
from ReverseMap.rdict import rdict, rmap
from ReverseMap.reverse import ReverseMap


ReverseDict = ReverseMap
ConvertibleValue = Convertible
