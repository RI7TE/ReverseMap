from __future__ import annotations
import datetime as dt
import os
import sys

from pathlib import Path
from typing import TYPE_CHECKING

import ujson as json


sys.path.append(str(Path(__file__).absolute().parent))
if TYPE_CHECKING:
    import typing

import pickle

from collections.abc import Mapping

from _util import show


def _freeze(obj)-> typing.Any | int | float | str | bool | bytes | frozenset[tuple[typing.Any, typing.Any]] | tuple[typing.Any, ...]:
    """Recursively convert obj into a hashable representation."""
    if obj is None or isinstance(obj, (int, float, str, bool, bytes)):
        return obj
    if isinstance(obj, Mapping):
        return frozenset((_freeze(k), _freeze(v)) for k, v in obj.items())
    if isinstance(obj, (list, tuple, set)):
        return tuple(_freeze(i) for i in obj)
    # Fallback: pickle arbitrary objects to bytes
    try:
        return pickle.dumps(obj)
    except Exception:
        # Last resort: use repr
        return repr(obj)


class Convertible:
    __slots__ = ('_frozen','_original')

    def __init__(self, original):
        self._original = original
        self._frozen = _freeze(original)

    def __hash__(self) -> int:
        return hash(self._frozen)

    def __eq__(self, other) -> typing.Any | bool:
        if not isinstance(other, Convertible) and isinstance(other, type(self._original)):
            return self._frozen == _freeze(other)
        return isinstance(other, Convertible) and self._frozen == other._frozen

    @property
    def as_key(self) -> typing.Any | int | float | str | bool | bytes | frozenset[tuple[typing.Any, typing.Any]] | tuple[typing.Any, ...]:
        return self._frozen

    def revert(self) -> typing.Any:
        """Return the original object."""
        return self._original

    def __repr__(self) -> str:
        return f"Convertible({self._original!r})"

    def __str__(self) -> str:
        return f"Convertible({self._original})"

    def __getstate__(self):
        return self._frozen, self._original

    def __get__(self, instance, owner=None):
        show("Convertible.__get__ called", instance, owner)
        if instance is None:
            return self.as_key
        return self._original

def convertible(value) -> Convertible:
    """
    Wrap value in Convertible (if not already), making it hashable
    and able to revert back to original.
    """
    return value if isinstance(value, Convertible) else Convertible(value)

