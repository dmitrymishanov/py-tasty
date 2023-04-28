from src.asserts import assert_eq, assert_true
from src.case import Case
from src.suite import Suite


def test_suite():
    # arrange
    def success():
        assert_eq(2 + 2, 4)
    success_case_1 = Case(success)
    success_case_2 = Case(success)

    def failure():
        assert_eq(2 + 2, 5)
    failure_case = Case(failure)

    def error():
        1 / 0
    error_case = Case(error)

    suite = Suite(cases=[success_case_1, success_case_2, failure_case, error_case])

    # act
    suite.run()

    # assert
    assert_true(suite.ran)
    assert_eq(suite.success, 2)
    assert_eq(suite.failure, 1)
    assert_eq(suite.errors, 1)


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
    assert_eq(suite.success, 1)
    assert_eq(suite.errors, 1)
