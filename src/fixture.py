from collections.abc import Callable
from typing import Any

fixture_registry = {
    'session': {},
    'function': {},
}
session_fixtures_cache = {}


def fixture(fixture_func: Callable | None = None, /, *, scope: str = 'function') -> Callable | None:
    if not fixture_func:
        def wrapper(fixture_func: Callable) -> None:
            fixture_registry[scope][fixture_func.__name__] = fixture_func

        return wrapper

    fixture_registry[scope][fixture_func.__name__] = fixture_func


class FixtureNotFound(Exception):
    def __init__(self, name: str) -> None:
        self.msg = f'Fixture {name} not found'


def get_fixture(name: str) -> Any:
    try:
        if name in fixture_registry['session']:
            return session_fixtures_cache.setdefault(name, fixture_registry['session'][name]())
        return fixture_registry['function'][name]()
    except KeyError:
        raise FixtureNotFound(name)
