from convert import Convertible, convertible
from icecream import ic
from rdict import rdict
from reverse import ReverseDictItems, ReverseDictKeys, ReverseDictValues, ReverseMap

from _util import show


def test_rdict():
    test_dict = rdict()
    test_dict['a'] = 1
    test_dict['b'] = 2
    test_dict['c'] = 3
    test_dict['d'] = 4
    test_dict['e'] = 5
    # Test the __contains__ method
    ic('a' in test_dict)  # True
    ic(1 in test_dict)    # True
    ic('f' in test_dict)  # False
    # Test the __setitem__ method
    test_dict['f'] = 6
    ic(test_dict['f'])    # 6
    # Test the invert method
    inverted_dict = test_dict.invert()
    ic(inverted_dict['a'])  # 1
    show(inverted_dict)
    ic(inverted_dict[1])    # 'a'
    # Test the __delitem__ method
    del test_dict['a']
    ic('a' in test_dict)  # False
    ic(1 in test_dict)    # True
    # Test the __getitem__ method
    ic(test_dict['b'])  # 2
    ic(test_dict[2])    # 'b'
    # Test the __getitem__ method with a non-existent key
    try:
       ic(test_dict['x'])  # Should raise KeyError
    except KeyError as e:
        ic(e)  # Key x not found in ReverseDict.
    # Test the __delitem__ method with a non-existent key
    try:
        del test_dict['x']  # Should raise KeyError
    except KeyError as e:
        ic(e)  # Key x not found in ReverseDict.
    # Test the __setitem__ method with an existing key
    test_dict['b'] = 20
    ic(test_dict['b'])  # 20
    # Test the __setitem__ method with a new key
    test_dict['f'] = 30
    ic(test_dict['f'])  # 30
    # Test the __contains__ method with a new key
    ic('f' in test_dict)  # True
    ic(30 in test_dict)    # True
    # Test the __contains__ method with a non-existent key
    ic('x' in test_dict)  # False
    ic(100 in test_dict)  # False
    # Test the __contains__ method with an existing value
    ic(20 in test_dict)  # True
    ic(30 in test_dict)  # True
    # Test the __contains__ method with a non-existent value
    ic(100 in test_dict)  # False
    # Test the __contains__ method with a key that exists in the inverse
    inverted_dict = test_dict.invert()
    ic('b' in inverted_dict)  # True
    ic(20 in inverted_dict)    # True
    ic('x' in inverted_dict)  # False
    ic(100 in inverted_dict)  # False
    # Test the __contains__ method with a value that exists in the inverse
    ic(inverted_dict['b'])  # 20
    ic(inverted_dict[20])    # 'b'
    # Test the __contains__ method with a value that does not exist in the inverse
    ic(inverted_dict.get('x'))  # None
    ic(inverted_dict.get(100))  # None
    #test the inverse property
    ic(test_dict)
    ic(test_dict.inverse)  # Should return the inverse dictionary
    ic(inverted_dict.inverse)  # Should return the inverse dictionary
    ic(test_dict.inverse == inverted_dict)  # Should be True
    ic(test_dict == inverted_dict.invert())  # True
    return True

def test():
    rd = ReverseMap(
        {'x': 'apple', 'y': 'banana', 'z': ['cherry', 'date', "fig", [{444.0, 555.0}]]}
    )
    rd['a'] = 1
    rd['b'] = 2
    rd['c'] = [3, rd['a'], {'d': rd['b']}]

    show(rd)  # {'a': 1, 'b': 2, 'c': 3}
    show(str(rd))  # {'a': 1, 'b': 2, 'c': 3}
    show(rd.inverse)  # {1: 'a', 2: 'b', 3: 'c'}
    show(str(rd.inverse))  # {1: 'a', 2: 'b', 3: 'c'}

    show(rd['a'])  # 1
    show(rd.inverse[1])  # 'a'

    rd['d'] = 4
    show(rd)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

    inv_rd = rd.invert()
    show(inv_rd)  # {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    show(inv_rd['a'])  # 1
    return True, "test"


def test_fnc():
    rd = ReverseMap()
    rd['x'] = 'apple'
    rd['y'] = 'banana'
    rd['z'] = 'cherry'

    show(rd)  # {'x': 'apple', 'y': 'banana', 'z': 'cherry'}
    show(rd.inverse)  # {'apple': 'x', 'banana': 'y', 'cherry': 'z'}

    show(rd['x'])  # apple
    show(rd.inverse['apple'])  # x

    rd['w'] = 'date'
    show(rd)  # {'x': 'apple', 'y': 'banana', 'z': 'cherry', 'w': 'date'}

    inv_rd = rd.invert()
    show(inv_rd)  # {'apple': 'x', 'banana': 'y', 'cherry': 'z', 'date': 'w'}
    show(inv_rd['x'])  # w
    show(rd.keys())
    show(rd.values())
    show(rd.items())
    show("In Keys", rd._inverse_keys)
    show("Inverse Values", rd._inverse_values)
    show("Inverse Items", rd._inverse_items)
    show("REVERSED", list(reversed(rd)))  # ['w', 'z', 'y', '
    show("REVERSED KEYS", list(reversed(rd._inverse_keys)))  # ['w', 'z', 'y', 'x']
    show(
        "REVERSED VALUES", list(reversed(rd._inverse_values))
    )  # ['date', 'cherry', 'banana', 'apple']
    show(
        "REVERSED ITEMS", list(reversed(rd._inverse_items))
    )  # [('w', 'date'), ('z', 'cherry'), ('y', 'banana'), ('x', 'apple')]
    show(
        "CONVERTIBLE DICT", rd._convertible_map
    )  # {Convertible('apple'): 'x', Convertible('banana'): 'y', Convertible('cherry'): 'z', Convertible('date'): 'w'}

    return True, "test_fnc"


def test2():
    d = {}
    key = convertible([1, 2, {'a': 3}])
    d[key] = "payload"
    # Use the Convertible as dict key
    show(d)  # {Convertible([1, 2, {'a': 3}]): 'payload'}
    # Revert to original
    orig = next(iter(d)).revert()
    show(orig, type(orig))
    return True, "test2"


def test_reverse_dict():
    rd = ReverseMap()
    rd['key1'] = 'value1'
    rd['key2'] = 'value2'
    rd['key3'] = 'value3'

    show("Original ReverseMap:", rd)
    show("Inverse:", rd.inverse)

    # Test getting items
    show("Get key1:", rd['key1'])
    show("Get value1 from inverse:", rd.inverse['value1'])

    # Test inversion
    inv_rd = rd.invert()
    show("Inverted ReverseMap:", inv_rd)
    return True, "test_reverse_dict"


def test_reverse_dict_items():
    rd = ReverseMap()
    rd['key1'] = 'value1'
    rd['key2'] = 'value2'

    items = ReverseDictItems(rd)
    show("ReverseDictItems:", list(items))

    # Test item retrieval
    for item in items:
        show("Item key:", item.key, "Item value:", item.value)
        inverse = rd._inverse
        _inverse_keys = ReverseDictKeys(rd)
        _inverse_values = ReverseDictValues(rd)
        _inverse_items = ReverseDictItems(rd)
        show("Inverse key:", inverse[item.value], "Inverse value:", item.key)
        show("Inverse Keys:", list(_inverse_keys))
        show("Inverse Values:", list(_inverse_values))
        show("Inverse Items:", list(_inverse_items))
    return True, "test_reverse_dict_items"


def test_reverse_dict_keys():
    rd = ReverseMap()
    rd['key1'] = 'value1'
    rd['key2'] = 'value2'

    keys = ReverseDictKeys(rd)
    show("ReverseDictKeys:", list(keys))

    # Test key retrieval
    for key in keys:
        show("Key:", key)
        inverse = rd.inverse
        show("INVERESE", inverse)
        show("Inverse value for key:", rd[key])
    return True, "test_reverse_dict_keys"


def test_reverse_dict_values():
    rd = ReverseMap()
    rd['key1'] = 'value1'
    rd['key2'] = 'value2'

    values = ReverseDictValues(rd)
    show("ReverseDictValues:", list(values))

    # Test value retrieval
    for value in values:
        show("Value:", value)
        inverse = rd.inverse
        show("Inverse key for value:", inverse[value])
    return True, "test_reverse_dict_values"


def test_convertible():
    d = {}
    _test_key = [1, 2, {'a': 3}]
    key = convertible([1, 2, {'a': 3}])
    show("KEY TYPE:", type(key))  # Convertible
    show("KEY Equality with revert:", key.revert() == _test_key)  # Convertible
    show("KEY Equality:", key == _test_key)  # Convertible
    d[key] = "payload"
    # Use the Convertible as dict key
    show("DICTIONARY: ", d) # {Convertible([1, 2, {'a': 3}]): 'payload'}
    # Revert to original
    orig = next(iter(d)).revert()
    show("ORIGINAL with type: ",orig, type(orig))  # [1, 2, {'a': 3}] <class 'list'>
    show("Hash of key:", hash(key))  # Hash
    show("KEY", key)
    show("KEY.askey", key.as_key)
    show("KEY.original", key._original)
    show("KEY.frozen", key._frozen)
    show("KEY.revert", key.revert())  # [1, 2, {'a': 3}]
    #__getstate__ test
    state = key.__getstate__()
    show("State of Convertible:", state)  # (frozen, original)
    # Recreate Convertible from state
    new_key = Convertible(state[1])
    show("New Convertible from state:", new_key)  # Convertible([1, 2, {'a': 3}])
    show("New Convertible revert:", new_key.revert())
    # Test __get__ method
    class TestClass:
        def __init__(self):
            self.convertible = key

        def get_convertible(self):
            return self.convertible
    test_instance = TestClass()
    show("TestClass instance convertible:", test_instance.convertible)  # Convertible([1, 2, {'a': 3}])
    show("TestClass instance convertible revert:", test_instance.convertible.revert())  # [1, 2, {'a': 3}]
    return True, "test_convertible"

def test_convertible1():
    d = {}
    _test_key = [1, 2, {'a': 3}]
    key = convertible([1, 2, {'a': 3}])
    show("KEY TYPE:", type(key))  # Convertible
    show("KEY Equality with revert:", key.revert() == _test_key)  # Convertible
    show("KEY Equality:", key == _test_key)  # Convertible
    d[key] = "payload"
    # Use the Convertible as dict key
    show("DICTIONARY: ", d)  # {Convertible([1, 2, {'a': 3}]): 'payload'}
    # Revert to original
    orig = next(iter(d)).revert()
    show("ORIGINAL with type: ", orig, type(orig))  # [1, 2, {'a': 3}] <class 'list'>
    show("Hash of key:", hash(key))  # Hash
    show("KEY", key)
    show("KEY.as_key", key.as_key)
    show("KEY.original", key._original)
    show("KEY.frozen", key._frozen)
    show("KEY.revert", key.revert())  # [1, 2, {'a': 3}]
    # __getstate__ test
    state = key.__getstate__()
    show("State of Convertible:", state)  # (frozen, original)
    # Recreate Convertible from state
    new_key = Convertible(state[1])
    show("New Convertible from state:", new_key)  # Convertible([1, 2, {'a': 3}])
    show("New Convertible revert:", new_key.revert())

    # Test __get__ method
    class TestClass:
        def __init__(self):
            self.convertible = key

        def get_convertible(self):
            return self.convertible

    test_instance = TestClass()
    show(
        "TestClass instance convertible:", test_instance.convertible
    )  # Convertible([1, 2, {'a': 3}])
    return True, "test_convertible1"


def test_chainmap():
    rd = ReverseMap()
    rd['key1'] = 'value1'
    rd['key2'] = 'value2'

    # Create a ChainMap with the ReverseMap and an additional dictionary
    additional_dict = {'key3': 'value3'}
    chain_map = rd.map.new_child(ReverseMap(additional_dict))

    show("ChainMap:", chain_map)
    show("ChainMap keys:", list(chain_map.keys()))
    show("ChainMap values:", list(chain_map.values()))
    show("ChainMap items:", list(chain_map.items()))
    return True, "test_chainmap"


def run_tests():
    results = []
    tests = [
        test(),
        test2(),
        test_fnc(),
        test_reverse_dict(),
        test_reverse_dict_items(),
        test_reverse_dict_keys(),
        test_reverse_dict_values(),
        test_convertible(),
        test_convertible1(),
        test_chainmap(),
        test_rdict(),
    ]
    for t in tests:
        if not t:
            results.append((f"A test failed: {t}",False))
            show(f"A test failed: {t}", color='yellow')
        else:
            results.append((f"Test {t} passed.", True))
    if all(result[1] for result in results):
        show("All tests passed successfully.")
    else:
        for result in results:
            show([d for d in result if d is False], color='red')
    show(results)


if __name__ == "__main__":
    run_tests()
