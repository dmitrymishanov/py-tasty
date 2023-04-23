from src.case import Case, CaseStatus


def test_case__ok():

    def my_owesome_test_case():
        assert 2 + 2 == 4

    case = Case(my_owesome_test_case)
    case.run()
    assert case.ran
    assert case.status is CaseStatus.success


def test_case__failed():

    def my_owesome_test_case():
        assert 2 + 2 == 5

    case = Case(my_owesome_test_case)
    case.run()
    assert case.ran
    assert case.status is CaseStatus.failed
    assert case.error == 'assert (2 + 2) == 5'
