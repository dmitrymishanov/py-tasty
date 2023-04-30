from src.asserts import assert_eq, assert_isinstance, assert_raises
from src.case import Case
from src.parametrize import (BadParamsSize, ParametrizedProxy, UnexpectedParam,
                             Variant, parametrize)


def test_parametrized_case_generates_multiple_cases():
    # arrange
    def test_with_params(denominator, divider):
        denominator / divider

    # act

    parametrized_test_with_params = parametrize(
        ['denominator', 'divider'], Variant(name='ok_test', params=[1, 1]), Variant(name='error_test', params=[1, 0])
    )(test_with_params)

    # assert
    assert_isinstance(parametrized_test_with_params, ParametrizedProxy)
    assert_eq(
        parametrized_test_with_params.cases,
        [
            Case(test_func=test_with_params, suffix='ok_test', params={'denominator': 1, 'divider': 1}),
            Case(test_func=test_with_params, suffix='error_test', params={'denominator': 1, 'divider': 0}),
        ],
    )


@parametrize(
    ['param_values'],
    Variant(
        'not_enough',
        [
            [
                1,
            ]
        ],
    ),
    Variant('too_many', [[1, 2, 3]]),
)
def test_parametrize__checks_that_variant_has_all_params(param_values):
    # arrange

    # act & assert
    with assert_raises(BadParamsSize) as e:
        parametrize(['foo', 'bar'], Variant('some_name', params=param_values))
    assert_eq(e.value.msg, f'Bad params size for variant=some_name. Expected: 2, actual: {len(param_values)}.')


def test_parametrize__checks_that_test_func_has_such_params():
    # arrange
    def test_func(first, second):
        ...

    # act & assert
    with assert_raises(UnexpectedParam) as e:
        parametrize(['second', 'third'], Variant('some_name', params=[..., ...]))(test_func)
    assert_eq(e.value.msg, f'Unexpected param third for test_func')
