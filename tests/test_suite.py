from src.case import Case
from src.suite import Suite


def test_suite():
    # arrange
    def success():
        assert 2 + 2 == 4
    success_case_1 = Case(success)
    success_case_2 = Case(success)

    def failure():
        assert 2 + 2 == 5
    failure_case = Case(failure)

    suite = Suite(cases=[success_case_1, success_case_2, failure_case])

    # act
    suite.run()

    # assert
    assert suite.ran
    assert suite.success == 2
    assert suite.failure == 1
