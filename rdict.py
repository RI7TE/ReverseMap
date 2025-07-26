
from __future__ import annotations
import os
import re
import sys

from pathlib import Path
from typing import Any, Hashable, Mapping, Sequence



sys.path.append(str(Path(__file__).absolute().parent))
from enum import Enum

from convert import Convertible, convertible
from reverse import ReverseMap, ReverseDictItems, ReverseDictKeys, ReverseDictValues
from _util import show


class _KeyType(Enum):
    """
    Enum to conserve the type of the value converted to a key used in reverse dictionary.
    """
    STR = str # Can be used as key
    INT = int # Can be used as key
    FLOAT = float # Can be used as key
    BOOL = bool # Can be used as key
    TUPLE = tuple # Can be used as key
    BYTES = bytes # Can be used as key


    def __call__(self, value: Any) -> Any:
        """
        Convert the value to the type represented by this KeyType.
        """
        return self.value(value)

    def __get__(self, obj, other=None):
        return self.value


KeyType = _KeyType | str | int | float | bool | tuple | bytes | Hashable




def rdict(*args:Mapping | Sequence[Mapping], **kwds) -> ReverseMap:
    """
    Create a new ReverseMap instance.
    """
    return ReverseMap(*args, **kwds)


def converter(value: Any) -> Convertible:
    """
    Convert a value to a Convertible instance.
    """
    return Convertible(value)
