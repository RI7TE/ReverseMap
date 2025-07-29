from __future__ import annotations
import sys

from pathlib import Path


sys.path.append(str(Path(__file__).absolute().parent))

from collections import ChainMap, OrderedDict
from collections.abc import Iterable, Reversible, Mapping, Iterator, Generator
from typing import Any, NamedTuple

from convert import Convertible, convertible


class ReverseDictError(Exception):
    """Custom exception for ReverseMap errors."""


class ReverseDictItem(NamedTuple):
    """
    A named tuple to represent items in ReverseMap.
    It contains the key and value, both as Convertible.
    """

    key: Convertible
    value: Convertible | Any

    def revert(self) -> tuple[Any, Any]:
        """
        Revert the key and value to their original types.
        """
        return self.key.revert() if isinstance(
            self.key, Convertible
        ) else self.key, self.value.revert() if isinstance(
            self.value, Convertible
        ) else self.value

    def __call__(self) -> ReverseDictItem:
        """
        Update the ReverseDictItem with a new ReverseMap.
        """
        return self.revert()


class ReverseDictItems(Iterable):
    """
    An iterable class to represent items in ReverseMap.
    It yields ReverseDictItem instances.
    """

    def __init__(self, reverse_dict: Mapping):
        self._reverse_dict = reverse_dict
        self._items = self._reverse_dict.items()

    def __contains__(self, item):
        if isinstance(item, Convertible):
            return item in list(self._items) or item.revert() in list(self._items)
        return item in list(self._items)

    def __getitem__(self, item) -> ReverseDictItem:
        return list(self._items).pop(item)

    def __iter__(self) -> Iterator[ReverseDictItem]:
        for key, value in self._items:
            yield ReverseDictItem(
                key=key if isinstance(key, Convertible) else convertible(key),
                value=value if isinstance(value, Convertible) else convertible(value),
            )

    def __len__(self) -> int:
        return len(self._items)

    def __str__(self) -> str:
        return f"ReverseDictItems({list(self._items)})"

    def __call__(self, reverse_dict: Mapping) -> ReverseDictItems:
        """
        Update the ReverseDictItems with a new ReverseMap.
        """
        self._reverse_dict = reverse_dict
        self._items = self._reverse_dict.items()
        return self


class ReverseDictKeys(Iterable):
    """
    An iterable class to represent keys in ReverseMap.
    It yields the original keys from the Convertible keys.
    """

    def __init__(self, reverse_dict: Mapping):
        self._reverse_dict = reverse_dict
        self._keys = self._reverse_dict.keys()

    def __iter__(self) -> Iterator[Any]:
        return iter(self._keys)

    def __len__(self) -> int:
        return len(self._keys)

    def __contains__(self, item) -> bool:
        if isinstance(item, Convertible):
            return (item.revert()) in list(self) or item in list(self)
        return item in list(self)

    def __getitem__(self, item) -> Any:
        return list(self._reverse_dict.keys()).pop(item)

    def __str__(self) -> str:
        return f"ReverseDictKeys({list(self._reverse_dict.keys())})"

    def __call__(self, reverse_dict: Mapping) -> ReverseDictKeys:
        self._reverse_dict = reverse_dict
        self._keys = self._reverse_dict.keys()
        return self


class ReverseDictValues(Iterable):
    """
    An iterable class to represent values in ReverseMap.
    It yields the original values from the Convertible values.
    """

    def __init__(self, reverse_dict: Mapping):
        self._reverse_dict = reverse_dict
        self._values = list(self._reverse_dict.values())

    def __iter__(self) -> Generator[Any, Any, None]:
        for value in list(self._values):
            yield value.revert() if isinstance(value, Convertible) else value

    def __len__(self) -> int:
        return len(self._values)

    def __contains__(self, item) -> bool:
        if isinstance(item, Convertible):
            return (item.revert()) in self._values or item in self._values
        return item in self._values

    def __getitem__(self, item) -> Any:
        return list(self._values).pop(item)

    def __str__(self) -> str:
        return f"ReverseDictValues({list(self._values)})"

    def __call__(self, reverse_dict: Mapping) -> ReverseDictValues:
        self._reverse_dict = reverse_dict
        self._values = self._reverse_dict.values()
        return self


class ReverseMap(dict, Reversible):
    """A dictionary that maintains a reverse mapping of keys to values. Including support for non-hashable keys using Convertible; providing additional functionality for reverse lookups.
    Supports case-insensitive keys and values, and allows for verbose output during lookups.

    Args:
        *args: Positional arguments to initialize the dictionary.
        **kwargs: Keyword arguments to initialize the dictionary.
    Attributes:
        _case_sensitive (bool): Whether the keys are case-sensitive. Defaults to True.
        _verbose (bool): Whether to print verbose output during lookups. Defaults to False.

    Raises:
        KeyError: If a key is not found in the dictionary.


    Returns:
        _type_: _description_

    Yields:
        _type_: _description_
    """

    _case_sensitive = True
    _verbose = False

    def __init__(self, *args, **kwargs):
        self._case_sensitive = kwargs.pop('_case_sensitive', True)
        self._verbose = kwargs.pop('_verbose', False)
        if not self._case_sensitive:
            # Convert all keys to lowercase if case sensitivity is off
            if (
                args
                and isinstance(args, tuple)
                and len(args) == 1
                and isinstance(args[0], dict)
            ):
                args = (
                    OrderedDict(
                        (k.lower(), v) if isinstance(k, str) else OrderedDict(k, v)
                        for k, v in args[0].items()
                    ),
                )
            elif (
                args
                and isinstance(args, tuple)
                and len(args) == 1
                and isinstance(args[0], list | tuple | set | frozenset)
            ):
                args = OrderedDict((str(k), v) for k, v in enumerate(list(args[0])))
            elif (
                args
                and isinstance(args, tuple)
                and len(args) == 2
                and isinstance(args[0], list | tuple | set | frozenset)
                and isinstance(args[1], list | tuple | set | frozenset)
            ):
                args = (OrderedDict((str(k), v) for k, v in zip(args[0], args[1])),)
            elif args and isinstance(args, dict):
                args = (
                    OrderedDict(
                        (k.lower(), v) if isinstance(k, str) else (k, v)
                        for k, v in args.items()
                    ),
                )
            if kwargs:
                for k, v in kwargs.items():
                    if isinstance(k, str):
                        k = k.casefold()
                    kwargs[k] = v
        super().__init__(*args, **kwargs)
        self._inverse = OrderedDict()
        for k, v in self.items():
            if not isinstance(v, Convertible):
                self._inverse[convertible(v)] = k
            else:
                self._inverse[v] = k
        self._inverse_keys: ReverseDictKeys = ReverseDictKeys(self._inverse)
        # print("Init Inverse Keys:", self._inverse_keys)
        self._inverse_values = ReverseDictValues(self._inverse)
        # print("Init Inverse Values:", self._inverse_values)
        self._inverse_items = ReverseDictItems(self._inverse)
        # print("Init Inverse Items:", self._inverse_items)
        self._convertible_map = OrderedDict(
            {convertible(v): k for k, v in self._inverse_items}
        )
        self.map = ChainMap(self, self._convertible_map, self._inverse)
        # print("Init Convertible Dict:", self._convertible_map)
        # print("Init ReverseMap-INVERSE:", self._inverse)
        # print("Init ReverseMap-CURRENT:", self.map.maps[0])
        # print("Init ReverseMap-ROOT:", self.map.maps[-1])
        # print("Init ReverseMap-ENCOLSING:", self.map.parents)
        # print("Init ReverseMap-MAP:", self.map)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._inverse[convertible(value)] = key
        self._inverse_keys = self._inverse_keys(self._inverse)
        self._inverse_values = self._inverse_values(self._inverse)
        self._inverse_items = self._inverse_items(self._inverse)
        if not isinstance(key, Convertible):
            key = convertible(key)
        if not isinstance(value, Convertible):
            value = convertible(value)
        self._convertible_map[key] = value

    def __getitem__(self, key):
        ck = key if isinstance(key, Convertible) else convertible(key)
        key = key.revert() if isinstance(key, Convertible) else key
        item = None
        loc = None
        try:
            if ck in self._convertible_map:
                item = self._convertible_map[ck]
                loc = "convertible_map"
            elif ck in self._inverse:
                item = self._inverse[ck]
                loc = "inverse"
            elif key in self:
                item = super().__getitem__(key) or super().__getitem__(_key)
                loc = "super"
            if item is None:
                raise KeyError(f"Key {key} not found in ReverseMap.")
        except KeyError:
            if not self._case_sensitive and isinstance(key, str):
                # Try case-insensitive lookup
                _key = key.casefold()
                if _key in self._convertible_map:
                    item = self._convertible_map[_key]
                    loc = "convertible_map (case-insensitive)"
                elif _key in self._inverse:
                    item = self._inverse[_key]
                    loc = "inverse (case-insensitive)"
                elif _key in self:
                    item = super().__getitem__(_key)
                    loc = "super (case-insensitive)"
            if item is None:
                raise KeyError(f"Key {key} not found in ReverseMap.")
        if item is None:
            raise KeyError(f"Key {key} not found in ReverseMap.")
        elif item and self._verbose and loc:
            print(
                f"item found in: {str(loc).title()} | ", "Item:", item, "From Key:", key
            )
        return item.revert() if isinstance(item, Convertible) else item

    def __delitem__(self, key):
        super().__delitem__(convertible(key))
        if convertible(key) in self._inverse:
            del self._inverse[convertible(key)]
        if key in self._inverse_keys:
            del self._inverse_keys[key]
        if convertible(key) in self._convertible_map:
            del self._convertible_map[convertible(key)]
        if key in self._convertible_map:
            del self._convertible_map[key]
        self._inverse_keys = self._inverse_keys(self.inverse)
        self._inverse_values = self._inverse_values(self.inverse)
        self._inverse_items = self._inverse_items(self.inverse)
        self.map = ChainMap(self, self._convertible_map, self._inverse)

    def __contains__(self, key) -> bool:
        ck = convertible(key)
        return (
            ck in self._inverse_keys
            or ck in self._inverse_values
            or key in self._inverse_keys
            or key in self._inverse_values
        )

    def __iter__(self) -> Generator[Any, Any, None]:
        yield from list(self.keys()) + list(self._inverse_keys)

    def __len__(self) -> int:
        return len(self.keys())

    @property
    def inverse(self) -> ReverseMap:
        """
        mapping of wrapped keys → wrapped values, unwrapped back to originals
        """
        if self._inverse is None:
            _inverse = {}
            for item in self._inverse_items:
                _inverse[
                    item.key.revert() if isinstance(item.key, Convertible) else item.key
                ] = (
                    item.value.revert()
                    if isinstance(item.value, Convertible)
                    else item.value
                )
            self._inverse = ReverseMap(**_inverse)
        return self._inverse

    def invert(self) -> ReverseMap:
        """
        Return a new ReverseMap with keys/values swapped
        """
        inv = ReverseMap()
        for k, v in self.inverse.items():
            inv[v.revert() if isinstance(v, Convertible) else convertible(v)] = (
                k.revert()
            )
        return inv

    @property
    def inverse_keys(self) -> ReverseDictKeys:
        """
        Returns the keys of the inverse dictionary.
        """
        return self._inverse_keys

    @property
    def inverse_values(self) -> ReverseDictValues:
        """
        Returns the values of the inverse dictionary.
        """
        return self._inverse_values

    @property
    def inverse_items(self) -> ReverseDictItems:
        """
        Returns the items of the inverse dictionary.
        """
        return self._inverse_items

    @property
    def convertible_map(self) -> ReverseMap:
        """
        Returns the convertible dictionary.
        """
        return ReverseMap(self._convertible_map)

    def __reversed__(self) -> Iterator[ReverseDictKeys]:
        """
        Return a reversed iterator over the keys of the ReverseMap.
        """
        return iter(self._inverse_keys)

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return f"ReverseMap({super().__repr__()})"
