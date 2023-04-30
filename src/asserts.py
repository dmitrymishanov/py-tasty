# TODO maybe try to use import hook to rewrite asserts as pytest does
#  https://docs.pytest.org/en/7.1.x/how-to/writing_plugins.html#assertion-rewriting
#  https://peps.python.org/pep-0302/
#  https://stackoverflow.com/questions/43571737/how-to-implement-an-import-hook-that-can-modify-the-source-code-on-the-fly-using
from typing import Self


def assert_eq(left, right) -> None:
    assert left == right, f'Expected {left} == {right}'


def assert_is(left, right) -> None:
    assert left is right, f'Expected {left} to be {right}'


def assert_true(target) -> None:
    assert_is(target, True)


def assert_false(target) -> None:
    assert_is(target, False)


def assert_isinstance(instance, class_) -> None:
    assert isinstance(instance, class_), f'Expected {instance} to be instance of {class_}'


class assert_raises:
    value: Exception

    def __init__(self, expected_exc: type[Exception]):
        self.expected_exc = expected_exc

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool | None:
        assert exc_val, f'Expected to raise {self.expected_exc}'
        self.value = exc_val
        if isinstance(exc_val, self.expected_exc):
            return True
