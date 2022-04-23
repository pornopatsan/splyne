from typing import Any, Optional, List

from pydeck import Deck

DEFAULT_SKKIPPED_KEYS = ['id']


def mock_prepare_deck_class() -> None:
    def deck_to_json_mock(self: Deck, _, **kwargs) -> str:
        return self.to_json()
    Deck.to_html = deck_to_json_mock


def assert_equal_jsons(first: Any, second: Any, skip_keys: Optional[List[str]] = None):
    """
    Given two jsons of pydeck.Deck, return if they are equal
    >>> assert_equal_jsons({}, {})
    >>> assert_equal_jsons([], [])
    >>> assert_equal_jsons({'a': [1, 2, 3], 'b': 'foo'}, {'a': [1, 2, 3], 'b': 'foo'})
    >>> assert_equal_jsons({'a': [1, 2, 3], 'b': 'foo'}, {'a': [1, 2, 3], 'b': 'bar'}, skip_keys=['b'])

    >>> assert_equal_jsons({'a': [1, 2, 3], 'b': 'foo'}, {'a': [1, 2, 3], 'b': 'bar'})
    Traceback (most recent call last):
     ...
    AssertionError
    >>> assert_equal_jsons({'a': [1, 2, 3], 'b': 'foo'}, {'a': [1, 2, 3]})
    Traceback (most recent call last):
     ...
    AssertionError
    >>> assert_equal_jsons({'a': [1, 2, 3]}, {'a': [1, 2]})
    Traceback (most recent call last):
     ...
    AssertionError
    >>> assert_equal_jsons({'a': '1'}, {'a': 1})
    Traceback (most recent call last):
     ...
    AssertionError
    """
    if skip_keys is None:
        skip_keys = DEFAULT_SKKIPPED_KEYS
    assert type(first) == type(second)
    if isinstance(first, list) and isinstance(second, list):
        assert len(first) == len(second)
        for item1, item2 in zip(first, second):
            assert_equal_jsons(item1, item2, skip_keys=skip_keys)
    elif isinstance(first, dict) and isinstance(second, dict):
        first_keys, second_keys = sorted(first.keys()), sorted(second.keys())
        assert len(first_keys) == len(second_keys)
        for key1, key2 in zip(first_keys, second_keys):
            assert key1 == key2
            if key1 in skip_keys:
                continue
            assert_equal_jsons(first[key1], second[key2], skip_keys=skip_keys)
    else:
        assert first == second
