def test_ordering(testdir, django_testdir):
    """Verify that tests are run in the same order Django would run them."""
    testdir.create_test_module(
        '''
        from django.test import TestCase, TransactionTestCase
        import pytest

        @pytest.mark.django_db(transaction=True)
        def test_run_second_decorator():
            pass

        def test_run_second_fixture(transactional_db):
            pass

        class RunSecond(TransactionTestCase):
            def test_something(self):
                pass

        @pytest.mark.django_db
        def test_run_first_decorator():
            pass

        def test_run_first_fixture(db):
            pass

        class RunFirst(TestCase):
            def test_something(self):
                pass
        '''
    )

    # Run in subprocess to avoid errors due to attempting to clean up the test
    # environment twice in the same process.
    result = django_testdir.runpytest_subprocess('--verbose')

    assert result.ret == 0
    result.stdout.fnmatch_lines([
        '*test_run_first_decorator*',
        '*test_run_first_fixture*',
        '*RunFirst::test_something*',
        '*test_run_second_decorator*',
        '*test_run_second_fixture*',
        '*RunSecond::test_something*',
    ])
