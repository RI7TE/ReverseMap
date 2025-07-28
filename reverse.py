from __future__ import annotations
import sys

from pathlib import Path


sys.path.append(str(Path(__file__).absolute().parent))

from collections import ChainMap, OrderedDict
from collections.abc import Iterable, Reversible
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
        return self.key.revert() if isinstance(self.key, Convertible) else self.key, self.value.revert() if isinstance(self.value, Convertible) else self.value

    def __call__(self, key, value) -> ReverseDictItem:
        """
        Update the ReverseDictItem with a new ReverseMap.
        """
        return ReverseDictItem(
            key=key if isinstance(key, Convertible) else convertible(key),
            value=value if isinstance(value, Convertible) else convertible(value),
        )
class ReverseDictItems(Iterable):
    """
    An iterable class to represent items in ReverseMap.
    It yields ReverseDictItem instances.
    """
    def __init__(self, reverse_dict: ReverseMap):
        self._reverse_dict = reverse_dict
        self._items = self._reverse_dict.items()
    def __contains__(self, item):
        if isinstance(item, Convertible):
            return item in list(self) or item.revert() in list(self)
        return item in list(self)

    def __getitem__(self, item):
        return list(self._items).pop(item)

    def __iter__(self):
        for key, value in self._items:
            yield ReverseDictItem(
                key=key if isinstance(key, Convertible) else convertible(key),
                value=value if isinstance(value, Convertible) else convertible(value),
            )

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return f"ReverseDictItems({list(self._items)})"
    def __call__(self, reverse_dict: ReverseMap):
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
    def __init__(self, reverse_dict: ReverseMap):
        self._reverse_dict = reverse_dict
        self._keys = self._reverse_dict.keys()

    def __iter__(self):
        return iter(self._keys)

    def __len__(self):
        return len(self._keys)

    def __contains__(self, item):
        if isinstance(item, Convertible):
            return (item.revert()) in list(self._reverse_dict) or item in list(self._reverse_dict._inverse)
        return item in list(self._keys)

    def __getitem__(self, item):
        return list(self._reverse_dict.keys()).pop(item)

    def __str__(self):
        return f"ReverseDictKeys({list(self._reverse_dict.keys())})"
    def __call__(self, reverse_dict: ReverseMap):
        self._reverse_dict = reverse_dict
        self._keys = self._reverse_dict.keys()
        return self

class ReverseDictValues(Iterable):
    """
    An iterable class to represent values in ReverseMap.
    It yields the original values from the Convertible values.
    """
    def __init__(self, reverse_dict: ReverseMap):
        self._reverse_dict = reverse_dict
        self._values = list(self._reverse_dict.values())

    def __iter__(self):
        for value in list(self._values):
            yield value.revert() if isinstance(value, Convertible) else value

    def __len__(self):
        return len(self._values)

    def __contains__(self, item):
        values = list(self._values)
        if isinstance(item, Convertible):
            return (item.revert()) in values or item in values
        return item in values

    def __getitem__(self, item):
        print("ReverseDictValues.__getitem__ called with item:", item)
        return list(self._values).pop(item)

    def __str__(self):
        return f"ReverseDictValues({list(self._values)})"

    def __call__(self, reverse_dict: ReverseMap):
        self._reverse_dict = reverse_dict
        self._values = self._reverse_dict.values()
        return self

class ReverseMap(dict, Reversible):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._inverse = OrderedDict()
        for k, v in self.items():
            if not isinstance(v, Convertible):
                self._inverse[convertible(v)] = k
            else:
                self._inverse[v] = k
        self._inverse_keys: ReverseDictKeys = ReverseDictKeys(self)
        #print("Init Inverse Keys:", self._inverse_keys)
        self._inverse_values = ReverseDictValues(self)
        #print("Init Inverse Values:", self._inverse_values)
        self._inverse_items = ReverseDictItems(self)
        #print("Init Inverse Items:", self._inverse_items)
        self._convertible_map = OrderedDict({convertible(v): k for k, v in self._inverse_items})
        self.map = ChainMap(self, self._convertible_map, self._inverse)
        #print("Init Convertible Dict:", self._convertible_map)
        #print("Init ReverseMap-INVERSE:", self._inverse)
        #print("Init ReverseMap-CURRENT:", self.map.maps[0])
        #print("Init ReverseMap-ROOT:", self.map.maps[-1])
        #print("Init ReverseMap-ENCOLSING:", self.map.parents)
        #print("Init ReverseMap-MAP:", self.map)
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._inverse[convertible(value)] = key
        self._inverse_keys = self._inverse_keys(self)
        self._inverse_values = self._inverse_values(self)
        self._inverse_items = self._inverse_items(self)
        if not isinstance(key, Convertible):
            key = convertible(key)
        if not isinstance(value, Convertible):
            value = convertible(value)
        self._convertible_map[key] = value

    def __getitem__(self, key):
        ck = convertible(key)
        item = None
        loc = None
        if ck in self._convertible_map:
            item = self._convertible_map[ck]
            loc = "convertible_map"
        elif ck in self._inverse:
            item = self._inverse[ck]
            loc = "inverse"
        elif key in self:
            item = super().__getitem__(key)
            loc = "super"
        if item is None:
            raise KeyError(f"Key {key} not found in ReverseMap.")
        print(f"item found in: {str(loc).title()} | ", "Item:", item)
        return item.revert() if isinstance(item, Convertible) else item

    def __delitem__(self, key):
        super().__delitem__(convertible(key))

    def __contains__(self, key):
        ck = convertible(key)
        return ck in self._inverse_keys or ck in self.inverse or key in self._inverse_keys or key in self.inverse

    def __iter__(self):
        yield from list(self.keys()) + list(self._inverse_keys)

    def __len__(self):
        return len(self.keys())

    @property
    def inverse(self):
        """
        mapping of wrapped keys → wrapped values, unwrapped back to originals
        """
        if self._inverse is None:
            _inverse = {}
            for item in self._inverse_items:
                _inverse[item.key.revert() if isinstance(item.key, Convertible) else item.key] = item.value.revert() if isinstance(item.value, Convertible) else item.value
            self._inverse = ReverseMap(**_inverse)
        return self._inverse

    def invert(self):
        """
        Return a new ReverseMap with keys/values swapped
        """
        inv = ReverseMap()
        for k, v in self.inverse.items():
            inv[v.revert() if isinstance(v, Convertible) else convertible(v)] = k.revert()
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

    def __reversed__(self):
        """
        Return a reversed iterator over the keys of the ReverseMap.
        """
        return iter(self._inverse_keys)

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return f"ReverseMap({super().__repr__()})"
