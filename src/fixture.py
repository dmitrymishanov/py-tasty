from collections.abc import Callable
from typing import Any

# TODO scope (session, function, module)
fixture_registry = {}


def fixture(fixture_func: Callable) -> None:
    fixture_registry[fixture_func.__name__] = fixture_func


class FixtureNotFound(Exception):
    def __init__(self, name: str) -> None:
        self.msg = f'Fixture {name} not found'


def get_fixture(name: str) -> Any:
    try:
        return fixture_registry[name]()
    except KeyError:
        raise FixtureNotFound(name)
