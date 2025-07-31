from __future__ import annotations
import sys

from pathlib import Path
from typing import TYPE_CHECKING


sys.path.append(str(Path(__file__).absolute().parent))
if TYPE_CHECKING:
    import typing

import pickle

from collections.abc import Mapping

from ReverseMap._util import show


def _freeze(
    obj,
) -> (
    typing.Any
    | int
    | float
    | str
    | bool
    | bytes
    | frozenset[tuple[typing.Any, typing.Any]]
    | tuple[typing.Any, ...]
):
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
    __slots__ = ('_frozen', '_index', '_iterobject', '_original')

    def __init__(self, original):
        self._original = original
        self._frozen = _freeze(original)
        self._index = 0
        self._iterobject = iter((self.original, self.frozen))

    @property
    def iterobject(self):
        """Return the iterator object."""
        return self._iterobject

    @iterobject.setter
    def iterobject(self, value):
        """Set the iterator object."""
        if not isinstance(value, Iterable):
            raise TypeError("iterobject must be an iterable.")
        self._iterobject = iter(value)
        self._index = 0

    @property
    def original(self):
        """Return the original object."""
        return self._original

    @property
    def frozen(self):
        """Return the frozen representation."""
        return self._frozen

    @property
    def total(self) -> int:
        """Return the total number of items in the frozen representation."""
        return len(self.original)

    def __hash__(self) -> int:
        return hash(self._frozen)

    def __eq__(self, other) -> typing.Any | bool:
        if not isinstance(other, Convertible) and isinstance(
            other, type(self._original)
        ):
            return self._frozen == _freeze(other)
        return isinstance(other, Convertible) and self._frozen == other._frozen

    def __iter__(self) -> typing.Generator[list[typing.Any], None, None]:
        return self

    @property
    def index(self) -> int:
        """Return the current index in the frozen representation."""
        return self._index

    @index.setter
    def index(self, value: int):
        """Set the current index in the frozen representation."""
        if value < 0 or value >= self.total:
            raise IndexError("Index out of range.")
        self._index = value

    def __next__(self):
        """Return the next item in the frozen representation."""
        if self._index >= self.total - 1:
            raise StopIteration
        while True:
            try:
                self._index += 1
                next_obj = next(self._iterobject)
                show(f"Next object: {next_obj!r}")
                if isinstance(next_obj, Convertible):
                    show(f"Next object is Convertible: {next_obj!r}")
                    next_obj = next_obj.revert()
                    show(f"Next object reverted: {next_obj!r}")
                return next_obj
            except StopIteration:
                self._index = 0
                raise StopIteration("No more items in the iterator.")

    def __len__(self) -> int:
        return len(self._original)

    @property
    def as_key(
        self,
    ) -> (
        typing.Any
        | int
        | float
        | str
        | bool
        | bytes
        | frozenset[tuple[typing.Any, typing.Any]]
        | tuple[typing.Any, ...]
    ):
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

    # def __get__(self, instance, owner=None):
    #    show(f"Instance - {instance} - Getting Convertible value: {self._original!r}")
    #    return self.as_key if instance is None else self._original


def convertible(value) -> Convertible:
    """
    Wrap value in Convertible (if not already), making it hashable
    and able to revert back to original.
    """
    return value if isinstance(value, Convertible) else Convertible(value)
