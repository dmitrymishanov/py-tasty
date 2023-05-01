from src.asserts import assert_eq, assert_true
from src.case import Case, CaseStatus
from src.fixture import fixture
from src.suite import Suite


def success():
    assert_eq(2 + 2, 4)


def failure():
    assert_eq(2 + 2, 5)


def error():
    1 / 0


@fixture
def success_case_1():
    return Case(success)


@fixture
def success_case_2():
    return Case(success)


@fixture
def failure_case():
    return Case(failure)


@fixture
def error_case():
    return Case(error)


def test_suite(success_case_1, success_case_2, failure_case, error_case):
    # arrange
    suite = Suite(cases=[success_case_1, success_case_2, failure_case, error_case])

    # act
    suite.run()

    # assert
    assert_true(suite.ran)
    assert_eq(
        suite.results,
        {
            CaseStatus.success: 2,
            CaseStatus.failed: 1,
            CaseStatus.error: 1,
        },
    )


def test_suite__errors_doesnt_break_whole_suite():
    # arrange
    def error():
        1 / 0

    error_case = Case(error)

    def success():
        assert_eq(2 + 2, 4)

    success_case = Case(success)

    # error case is first
    suite = Suite(cases=[error_case, success_case])

    # act
    suite.run()

    # assert
    assert_eq(
        suite.results,
        {
            CaseStatus.success: 1,
            CaseStatus.failed: 0,
            CaseStatus.error: 1,
        },
    )
