from __future__ import annotations
import sys

from pathlib import Path


sys.path.append(str(Path(__file__).absolute().parent))

from collections import ChainMap, OrderedDict
from collections.abc import Iterable, Reversible, Mapping, Iterator, Generator
from typing import Any, NamedTuple, Self

from ReverseMap.convert import Convertible, convertible

from ReverseMap._util import show


class ReverseMappingError(Exception):
    """Custom exception for ReverseMap errors."""


class ReverseMapItem(NamedTuple):
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

    def __call__(self) -> tuple[Any, Any]:
        """
        Update the ReverseMapItem with a new ReverseMap.
        """
        return self.revert()


class ReverseMapItems(Iterable):
    """
    An iterable class to represent items in ReverseMap.
    It yields ReverseMapItem instances.
    """

    def __init__(self, reverse_dict: Mapping):
        self._reverse_dict = reverse_dict
        self._items = [
            ReverseMapItem(key=k, value=v) for k, v in self._reverse_dict.items()
        ]

    def __contains__(self, item):
        if isinstance(item, Convertible):
            return item in list(self._items) or item.revert() in list(self._items)
        return item in list(self._items)

    def __getitem__(self, item) -> ReverseMapItem:
        return list(self._items).pop(item)

    def __iter__(self) -> Iterator[ReverseMapItem]:
        for key, value in self._items:
            yield ReverseMapItem(
                key=key if isinstance(key, Convertible) else convertible(key),
                value=value if isinstance(value, Convertible) else convertible(value),
            )

    def __len__(self) -> int:
        return len(self._items)

    def __str__(self) -> str:
        return f"ReverseMapItems({list(self._items)})"

    def __call__(self, reverse_dict: Mapping) -> ReverseMapItems:
        """
        Update the ReverseMapItems with a new ReverseMap.
        """
        self._reverse_dict = reverse_dict
        self._items = [
            ReverseMapItem(key=k, value=v) for k, v in self._reverse_dict.items()
        ]
        return self

    def revert(self):
        """
        Convert the items to radians.
        """
        return [
            item.revert()
            for item in self._items
            if isinstance(item, Convertible | ReverseMapItem)
        ]


class ReverseMapKeys(Iterable):
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
        try:
            return list(self._keys).pop(item)
        except IndexError:
            raise IndexError(f"Index {item} out of range for ReverseMapKeys.") from None
        except TypeError:
            try:
                return list(self._keys).pop(list(self._keys).index(item))
            except ValueError:
                raise ValueError(f"Item {item} not found in ReverseMapKeys.") from None

    def __str__(self) -> str:
        return f"ReverseMapKeys({list(self._reverse_dict.keys())})"

    def __call__(self, reverse_dict: Mapping) -> ReverseMapKeys:
        self._reverse_dict = reverse_dict
        self._keys = self._reverse_dict.keys()
        return self


class ReverseMapValues(Iterable):
    """
    An iterable class to represent values in ReverseMap.
    It yields the original values from the Convertible values.
    """

    def __init__(self, reverse_dict: Mapping):
        self._reverse_dict = reverse_dict
        self._values = self._reverse_dict.values()

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
        try:
            return list(self._values).pop(item)
        except IndexError:
            raise IndexError(
                f"Index {item} out of range for ReverseMapValues."
            ) from None
        except TypeError:
            try:
                return list(self._values).pop(list(self._values).index(item))
            except ValueError:
                raise ValueError(
                    f"Item {item} not found in ReverseMapValues."
                ) from None

    def __str__(self) -> str:
        return f"ReverseMapValues({list(self._values)})"

    def __call__(self, reverse_dict: Mapping) -> ReverseMapValues:
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

    case_sensitive = True
    _verbose = False

    def __init__(self, *args, **kwds):
        self._caller = None
        _mydict = kwds.copy()
        for k, v in _mydict.items():
            if isinstance(k, str) and k.startswith('_'):
                # Handle special keys that start with an underscore
                if k == '_case_sensitive':
                    self.case_sensitive = kwds.pop(k, True)
                elif k == '_verbose':
                    self._verbose = kwds.pop(k, False)
                else:
                    setattr(self, k, kwds.pop(k))
        del _mydict
        self.case_sensitive = kwds.pop('_case_sensitive', True)
        self._verbose = kwds.pop('_verbose', False)
        if self._verbose:
            show(
                "ARGS TYPE:",
                [type(arg) for arg in args],
                "KWDS TYPE:",
                {type(k): type(v) for k, v in kwds.items()},
                "Case Sensitive:",
                self.case_sensitive,
                "Verbose:",
                self._verbose,
                term=True,
            )
        if not self.case_sensitive:
            # Convert all keys to lowercase if case sensitivity is off
            if (
                args
                and isinstance(args, tuple)
                and len(args) == 1
                and isinstance(args[0], dict | zip)
            ):
                args = OrderedDict(
                    (k.casefold(), v) if isinstance(k, str) else (k, v)
                    for k, v in dict(args[0]).items()
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
                args = OrderedDict((str(k), v) for k, v in zip(args[0], args[1]))
            elif args and isinstance(args, dict | zip):
                args = OrderedDict(
                    (k.lower(), v) if isinstance(k, str) else (k, v)
                    for k, v in dict(args).items()
                )
            if kwds:
                for k, v in kwds.items():
                    if isinstance(k, str):
                        k = k.casefold()
                    kwds[k] = v
        if self._verbose:
            show(
                f"Initializing ReverseMap with args: {args} and kwds: {kwds}",
                color="blue",
                term=True,
            )
        super().__init__(*args, **kwds)
        self._inverse = OrderedDict(
            {
                convertible(v): k
                for k, v in self.items()
                if not isinstance(v, Convertible)
            }
        )
        self._inverse_keys: ReverseMapKeys = ReverseMapKeys(self._inverse)
        self._inverse_values = ReverseMapValues(self._inverse)
        self._inverse_items = ReverseMapItems(self._inverse)
        self._convertible_map = OrderedDict(
            {convertible(v): k for k, v in self._inverse_items}
        )
        self._map = ChainMap(self, self._convertible_map, self._inverse)

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
        self._map = ChainMap(self, self._convertible_map, self._inverse)

    def __getitem__(self, key):
        item = None
        loc = None
        check_items = [
            key.revert() if isinstance(key, Convertible) else key,
            convertible(key) if not isinstance(key, Convertible) else key,
        ]
        if not self.case_sensitive and isinstance(key, str):
            # Check for case-insensitive keys
            check_items.extend(
                [
                    key.casefold(),
                    key.upper(),
                    key.title(),
                ]
            )
        if (
            not self.case_sensitive
            and isinstance(key, Convertible)
            and isinstance(key.revert(), str)
        ):
            check_items.extend(
                [
                    key.revert().casefold(),
                    key.revert().upper(),
                    key.revert().title(),
                ]
            )

        def check_mappings(key):
            nonlocal item, loc
            if self._verbose:
                show(
                    f"Checking mappings for key: {key!r} (case_sensitive={self.case_sensitive})"
                )
            if item := self._convertible_map.get(key):
                loc = (
                    "convertible_map"
                    if not self.case_sensitive
                    else "convertible_map (case-sensitive)"
                )
            elif item := self.get(key):
                loc = (
                    "instance"
                    if not self.case_sensitive
                    else "instance (case-sensitive)"
                )
            elif item := self._inverse.get(key):
                loc = (
                    "inverse" if not self.case_sensitive else "inverse (case-sensitive)"
                )
            elif item := self._map.get(key):
                loc = "map" if not self.case_sensitive else "map (case-sensitive)"
            elif item := self._inverse_values[key]:
                loc = (
                    "inverse_values"
                    if not self.case_sensitive
                    else "inverse_values (case-sensitive)"
                )
            elif item := self._inverse_items[key]:
                loc = (
                    "inverse_items"
                    if not self.case_sensitive
                    else "inverse_items (case-sensitive)"
                )
            elif item := self._inverse_keys[key]:
                loc = (
                    "inverse_keys"
                    if not self.case_sensitive
                    else "inverse_keys (case-sensitive)"
                )
            elif item := super().__getitem__(key):
                loc = (
                    "instance"
                    if not self.case_sensitive
                    else "instance (case-sensitive)"
                )
            return item, loc

        try:
            for item in check_items:
                item, loc = check_mappings(item)
                if item:
                    break
            if item is None:
                raise ReverseMappingError(f"Key {key} not found in ReverseMap.")
        except ReverseMappingError as e:
            show(f"Error: {e}", color="red", term=True)
            raise e
        except TypeError as e:
            show(f"TypeError: {e} - Key: {key!r}", color="red", term=True)
            raise TypeError(f"Key {key} is not hashable or convertible.") from e
        except ValueError as e:
            show(f"ValueError: {e} - Key: {key!r}", color="red", term=True)
            raise ValueError(f"Key {key} not found in ReverseMap.") from e
        except KeyError as e:
            show(f"KeyError: {e} - Key: {key!r}", color="red", term=True)
            # If the key is not found, raise a KeyError with a custom message
            raise KeyError(f"Key {key} not found in ReverseMap.") from e

        else:
            if item and self._verbose and loc:
                print(
                    f"item found in: {str(loc).title()} | ",
                    "Item:",
                    item,
                    "From Key:",
                    key,
                )
            return item.revert() if isinstance(item, Convertible) else item

    def _sync(self) -> Self:
        """Sync the internal state of the ReverseMap."""
        caller = self._caller
        if caller and caller != "inverse":
            self.inverse = {
                convertible(v): k
                for k, v in self.items()
                if not isinstance(v, Convertible)
            }
            if self._verbose:
                print("Inverse Mapping:", self.inverse)
        if caller and caller != "inverse-keys":
            self.inverse_keys = self._inverse_keys(self.inverse)
            if self._verbose:
                print("Inverse Keys: ", self.inverse_keys)
        if caller and caller != "inverse-values":
            self.inverse_values = self._inverse_values(self.inverse)
            if self._verbose:
                print("Inverse Values: ", self._inverse_values)
        if caller and caller != "inverse-items":
            self.inverse_items = self._inverse_items(self.inverse)
            if self._verbose:
                print("Inverse Items: ", self._inverse_items)
        if caller and caller != "convertible-map":
            self.convertible_map = OrderedDict(
                {convertible(v): k for k, v in self.inverse_items}
            )
            if self._verbose:
                print("Convertible Mapping:", self._convertible_map)
        if caller and caller != "map":
            self.map = ChainMap(self, self.convertible_map, self.inverse)
            if self._verbose:
                print("Combined Mapping:", self.map)
        self._caller = None
        return self

    def __setattr__(self, name, value):
        """Set an attribute on the ReverseMap."""
        if name in self.__dict__:
            super().__setattr__(name, value)
        else:
            # If the attribute is not already set, treat it as a key-value pair
            self.__dict__[name] = value

    def __delitem__(self, key):
        super().__delitem__(convertible(key))
        if convertible(key) in self:
            del self[convertible(key)]
        elif key in self:
            del self[key]
        self._sync()

    def __contains__(self, key) -> bool:
        check_items = [
            key.revert() if isinstance(key, Convertible) else key,
            convertible(key) if not isinstance(key, Convertible) else key,
        ]
        if not self.case_sensitive and isinstance(key, str):
            # Check for case-insensitive keys
            check_items.extend(
                [
                    key.casefold(),
                    key.upper(),
                    key.title(),
                ]
            )
        if (
            not self.case_sensitive
            and isinstance(key, Convertible)
            and isinstance(key.revert(), str)
        ):
            check_items.extend(
                [
                    key.revert().casefold(),
                    key.revert().upper(),
                    key.revert().title(),
                ]
            )
        ck = convertible(key) if not isinstance(key, Convertible) else key
        key = key.revert() if isinstance(key, Convertible) else key
        if inside := super().__contains__(ck) or super().__contains__(key):
            if self._verbose:
                show(f"Key {key} found in ReverseMap.")
            return inside

        def check_key(case_key):
            if (
                inside := case_key in self._convertible_map
                or case_key in self._inverse
                or case_key in self._inverse_keys
                or case_key in self._inverse_values
                or case_key in self._inverse_items
                or case_key in self.__dict__
            ):
                if self._verbose:
                    show(f"Key {case_key} found in ReverseMap (case-insensitive).")
                return inside
            return False

        for case_key in check_items:
            if inside := check_key(case_key):
                return inside
        if self._verbose:
            show(f"Key {key} not found in ReverseMap.")
        return False

    def __iter__(self) -> Generator[Any, Any, None]:
        yield from list(self.keys()) + list(self._inverse_keys)

    def __len__(self) -> int:
        return len(self.keys())

    @property
    def map(self) -> ChainMap:
        """
        Returns the combined mapping of the ReverseMap.
        """
        return self._map

    @map.setter
    def map(self, value: Mapping):
        """
        Sets the combined mapping of the ReverseMap.
        """
        self._caller = "map"
        self._map = ChainMap(self, value, self._convertible_map, self._inverse)
        self._sync()

    @property
    def inverse(self) -> ReverseMap:
        """
        mapping of wrapped keys → wrapped values, unwrapped back to originals
        """
        return self._inverse

    @inverse.setter
    def inverse(self, value: Mapping):
        self._caller = "inverse"
        self._inverse = ReverseMap(**value)
        self._sync()

    def invert(self) -> ReverseMap:
        """
        Return a new ReverseMap with keys/values swapped
        """
        inv = ReverseMap()
        for k, v in self.items():
            inv[convertible(v) if not isinstance(v, Convertible) else v] = (
                k.revert() if isinstance(v, Convertible) else k
            )
        return inv

    @property
    def inverse_keys(self) -> ReverseMapKeys:
        """
        Returns the keys of the inverse dictionary.
        """
        return self._inverse_keys

    @inverse_keys.setter
    def inverse_keys(self, value: ReverseMapKeys):
        """
        Sets the keys of the inverse dictionary.
        """
        self._caller = "inverse-keys"
        self._inverse_keys = value
        self._sync()

    @property
    def inverse_values(self) -> ReverseMapValues:
        """
        Returns the values of the inverse dictionary.
        """
        return self._inverse_values

    @inverse_values.setter
    def inverse_values(self, value: ReverseMapValues):
        """
        Sets the values of the inverse dictionary.
        """
        self._caller = "inverse-values"
        self._inverse_values = value
        self._sync()

    @property
    def inverse_items(self) -> ReverseMapItems:
        """
        Returns the items of the inverse dictionary.
        """
        return self._inverse_items

    @inverse_items.setter
    def inverse_items(self, value: ReverseMapItems):
        """
        Sets the items of the inverse dictionary.
        """
        self._caller = "inverse-items"
        self._inverse_items = value
        self._sync()

    @property
    def convertible_map(self) -> ReverseMap:
        """
        Returns the convertible dictionary.
        """
        return ReverseMap(self._convertible_map)

    @convertible_map.setter
    def convertible_map(self, value: Mapping):
        """
        Sets the convertible dictionary.
        """
        self._caller = "convertible-map"
        self._convertible_map = ReverseMap(**value)
        self._sync()

    def __reversed__(self) -> Iterator[ReverseMapKeys]:
        """
        Return a reversed iterator over the keys of the ReverseMap.
        """
        return iter(self._inverse_keys)

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return f"ReverseMap({super().__repr__()})"


type ReverseMapping = ReverseMap
