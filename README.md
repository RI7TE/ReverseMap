# ReverseMap

ReverseMap is a specialized Python dictionary that enables bidirectional lookups - you can search using either keys or values with the `in` operator. It handles non-hashable objects by automatically converting them to hashable representations while maintaining the ability to revert back to the original objects.

## Features

- **Bidirectional Lookups**: Search for keys by values and values by keys using the same interface
- **Support for Non-hashable Values**: Use lists, dictionaries, or custom objects as dictionary values
- **Convertible Objects**: Automatically converts non-hashable objects into hashable representations
- **Revertible**: Access original objects from their hashable representations
- **Dict-like Interface**: Familiar dictionary interface with extensions

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ReverseMap.git

# Navigate to the directory
cd ReverseMap

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from rdict import rdict

# Create a ReverseMap
rd = rdict()
rd['x'] = 'apple'
rd['y'] = 'banana'
rd['z'] = 'cherry'

# Look up by key (normal dictionary behavior)
print(rd['x'])  # Output: apple

# Look up by value (reverse lookup)
print(rd.inverse['apple'])  # Output: x

# Check membership with either keys or values
print('x' in rd)        # True
print('apple' in rd)    # True
```

### Using with Non-hashable Values

```python
from rdict import rdict

# Create a ReverseMap with non-hashable values
rd = rdict()
rd['a'] = [1, 2, 3]           # List as value
rd['b'] = {'key': 'value'}    # Dict as value
rd['c'] = set([4, 5, 6])      # Set as value

# Look up by key
print(rd['a'])  # Output: [1, 2, 3]

# Look up by value (automatically handles the conversion)
print(rd.inverse[[1, 2, 3]])  # Output: a
```

### Inverting a Dictionary

```python
from rdict import rdict

# Create a ReverseMap
rd = rdict({'x': 'apple', 'y': 'banana', 'z': 'cherry'})

# Invert the dictionary (swap keys and values)
inverted = rd.invert()

# Now keys are values and values are keys
print(inverted['apple'])  # Output: x
```

## API Reference

### `rdict(*args, **kwargs)`

Creates a new `ReverseMap` instance.

### `ReverseMap` Class

- **`__getitem__(key)`**: Gets the value for a key, or the key for a value
- **`__setitem__(key, value)`**: Sets a key-value pair
- **`__contains__(key)`**: Checks if a key or value exists
- **`inverse`**: Property that returns the inverse mapping
- **`invert()`**: Method that returns a new ReverseMap with keys and values swapped
- **`inverse_keys`**: Property that returns an iterable of the inverse keys
- **`inverse_values`**: Property that returns an iterable of the inverse values
- **`inverse_items`**: Property that returns an iterable of the inverse items

### `Convertible` Class

- **`revert()`**: Returns the original object
- **`as_key`**: Property that returns the hashable representation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Copyright © 2025 Steven Kellum
Licensed under the Personal Use License v1.0.
See LICENSE.txt for full terms. For commercial use, contact sk@perfectatrifecta.com
