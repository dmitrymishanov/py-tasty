from types import TracebackType

from src.case import Case, CaseStatus


def test_case__ok():
    # arrange
    def my_owesome_test_case():
        assert 2 + 2 == 4

    case = Case(my_owesome_test_case)

    # act
    case.run()

    # assert
    assert case.ran
    assert case.status is CaseStatus.success


def test_case__failed():
    # arrange
    def my_owesome_test_case():
        assert 2 + 2 == 5

    case = Case(my_owesome_test_case)

    # act
    case.run()

    # assert
    assert case.ran
    assert case.status is CaseStatus.failed
    assert case.failure_reason == 'assert (2 + 2) == 5'


def test_case__error():
    # arrange
    def error_test_case():
        1 / 0

    case = Case(error_test_case)

    # act
    case.run()

    # assert
    assert case.ran
    assert case.status is CaseStatus.error
    assert isinstance(case.tb, TracebackType)
