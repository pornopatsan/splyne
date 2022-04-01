import copy
import itertools

from typing import Iterable, Callable, Any, Dict


def make_pipe(*functions: Iterable[Callable[[Any], Any]]):
    """
    Create pipe of given fuctions
    This is **not** a decorator
    >>> squarer = lambda x: x*x
    >>> adder = lambda x: x+1
    >>> pipe1 = make_pipe(squarer, adder)
    >>> list(pipe1([1, 2, 3, 4]))
    [2, 5, 10, 17]
    >>> pipe2 = make_pipe(adder, squarer)
    >>> list(pipe2([1, 2, 3, 4]))
    [4, 9, 16, 25]
    """
    def wrapper(data: Iterable[Any]):
        for item in data:
            for func in functions:
                item = func(item)
            yield item
    return wrapper


def zip_into(
    items: Iterable[Dict[str, Any]],
    key: str,
    values: Any
) -> Iterable[Dict[str, Any]]:
    """
    Given an iterable of items and values of the same size.
    Make inerator, that sequentially inserts values into items on given key.
    Rewrites key if it already exists. 
    >>> data = [{'a': 1}, {'a': 2}, {'a': 3}]
    >>> list(zip_into(data, 'b', [3, 4, 5]))
    [{'a': 1, 'b': 3}, {'a': 2, 'b': 4}, {'a': 3, 'b': 5}]
    >>> data = [{'a': 1}, {'a': 2}, {'a': 3}]
    >>> list(zip_into(data, 'a', [10, 10, 10]))
    [{'a': 10}, {'a': 10}, {'a': 10}]
    >>> data = [{'a': 1}, {'a': 2, 'b': 4}, {'a': 3, 'c': 4}]
    >>> list(zip_into(data, 'c', [0, 1, 2]))
    [{'a': 1, 'c': 0}, {'a': 2, 'b': 4, 'c': 1}, {'a': 3, 'c': 2}]
    """
    for item, value in itertools.zip_longest(items, values):
        if item is None or value is None:
            raise ValueError("Items and Values must be of equal lengths")
        item.update({key: value})
        yield item


def merge(
    **kwargs: Dict[str, Iterable[Any]]
) -> Iterable[Dict[str, Any]]:
    """
    >>> list(merge(a=[1, 2, 3], b=[3, 4, 5]))
    [{'a': 1, 'b': 3}, {'a': 2, 'b': 4}, {'a': 3, 'b': 5}]
    """
    keys = list(kwargs.keys())
    for items in itertools.zip_longest(*kwargs.values()):
        if any(item is None for item in items):
            raise ValueError("Items sequences must be of equal lengths")
        yield dict(zip(keys, items))


def rename(
    items: Iterable[Dict[str, Any]],
    old_name: str,
    new_name: str,
    ignore_missing: bool = False
) -> Iterable[Dict[str, Any]]:
    """
    >>> data = [{'a': 1}, {'a': 2}, {'a': 3}]
    >>> list(rename(data, 'a', 'b'))
    [{'b': 1}, {'b': 2}, {'b': 3}]
    >>> data = [{'a': 1}, {'a': 2}, {'a': 3}]
    >>> list(rename(data, 'b', 'c', ignore_missing=True))
    [{'a': 1}, {'a': 2}, {'a': 3}]
    """
    for item in items:
        if old_name not in item:
            if not ignore_missing:
                raise ValueError(f"Key `{old_name}` does not exist")
        else:
            item[new_name] = item.pop(old_name)
        yield item
