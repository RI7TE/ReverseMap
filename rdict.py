
from __future__ import annotations
import sys

from collections.abc import Hashable, Mapping, Sequence
from pathlib import Path
from typing import Any


sys.path.append(str(Path(__file__).absolute().parent))
from enum import Enum

from _util import show
from convert import Convertible, convertible
from reverse import ReverseMap


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


def main(*args) -> ReverseMap:
    return rdict(*args)


def is_odd(n: float):
    return n % 2 == 1


def is_even(n: float):
    return n % 2 == 0

def print_from_args(argv):
    if len(argv) <= 1:
         raise ValueError("No arguments provided for main function")

    arg_dict = {}
    args = argv[1:]
    key = None
    val = None
    for index, arg in enumerate(args):
        if is_even(index):
            key = arg
        elif is_odd(index):
            val = arg
        if key and val:
            arg_dict[key] = val
            key = None
            val = None
    rd = main(arg_dict)
    print(rd)
    return rd

if __name__ == "__main__":
    try:
        rd = print_from_args(sys.argv)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    else:
        show(rd)
