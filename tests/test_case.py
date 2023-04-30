from types import TracebackType

from src.asserts import assert_eq, assert_is, assert_isinstance, assert_true
from src.case import Case, CaseStatus


def test_case__ok():
    # arrange
    def my_owesome_test_case():
        assert_eq(2 + 2, 4)

    case = Case(my_owesome_test_case)

    # act
    case.run()

    # assert
    assert_true(case.ran)
    assert_is(case.status, CaseStatus.success)


def test_case__failed():
    # arrange
    def my_owesome_test_case():
        assert_eq(2 + 2, 5)

    case = Case(my_owesome_test_case)

    # act
    case.run()

    # assert
    assert_true(case.ran)
    assert_is(case.status, CaseStatus.failed)
    assert_eq(case.failure_reason, 'Expected 4 == 5')


def test_case__error():
    # arrange
    def error_test_case():
        1 / 0

    case = Case(error_test_case)

    # act
    case.run()

    # assert
    assert_true(case.ran)
    assert_is(case.status, CaseStatus.error)
    assert_isinstance(case.tb, TracebackType)
