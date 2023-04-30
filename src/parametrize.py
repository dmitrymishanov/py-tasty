import inspect
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Callable

from src.case import Case


@dataclass
class Variant:
    name: str
    params: Sequence[Any]


class BadParamsSize(Exception):
    def __init__(self, *, variant_name: str, expected: int, actual: int) -> None:
        self.msg = f'Bad params size for variant={variant_name}. Expected: {expected}, actual: {actual}.'


class UnexpectedParam(Exception):
    def __init__(self, *, test_name: str, param_name: str) -> None:
        self.msg = f'Unexpected param {param_name} for {test_name}'


@dataclass
class ParametrizedProxy:
    test_func: Callable
    param_names: Sequence[str]
    variants: Sequence[Variant]

    @property
    def cases(self) -> list[Case]:
        cases = []
        for variant in self.variants:
            cases.append(
                Case(
                    test_func=self.test_func,
                    suffix=variant.name,
                    params={key: value for key, value in zip(self.param_names, variant.params)},
                )
            )
        return cases


def parametrize(param_names: Sequence[str], *variants: Variant) -> Callable:
    for variant in variants:
        if len(variant.params) != len(param_names):
            raise BadParamsSize(variant_name=variant.name, expected=len(param_names), actual=len(variant.params))

    def decorator(test_func: Callable) -> ParametrizedProxy:
        expected_params = inspect.getfullargspec(test_func).args
        for param in param_names:
            if param not in expected_params:
                raise UnexpectedParam(test_name=test_func.__name__, param_name=param)
        return ParametrizedProxy(test_func=test_func, param_names=param_names, variants=variants)

    return decorator
