"""
Approach inspired by https://github.com/pytest-dev/pytest-django/pull/223.
"""
import pytest
from django.test import TestCase, TransactionTestCase
from pytest_django.plugin import validate_django_db


# The ordering introduced in https://github.com/pytest-dev/pytest-django/pull/223
# is still wrong. Run last so we have the final say on ordering.
@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(items):
    def get_marker_transaction(test):
        try:
            marker = test.get_closest_marker('django_db')
        except AttributeError:
            # pytest < 3.6.0
            marker = test.get_marker('django_db')

        if marker:
            validate_django_db(marker)
            try:
                return marker.kwargs.get('transaction')
            except AttributeError:
                # pytest-django < 3.3.0
                return marker.transaction

        return None

    def has_fixture(test, fixture):
        fixturenames = getattr(test, 'fixturenames', None)
        return fixturenames and fixture in fixturenames

    def weight_test_case(test):
        """
        Key function for ordering test cases like the Django test runner.
        """
        is_test_case_subclass = test.cls and issubclass(test.cls, TestCase)
        is_transaction_test_case_subclass = test.cls and issubclass(test.cls, TransactionTestCase)

        if is_test_case_subclass or get_marker_transaction(test) is False:
            return 0
        elif has_fixture(test, 'db'):
            return 0

        if is_transaction_test_case_subclass or get_marker_transaction(test) is True:
            return 1
        elif has_fixture(test, 'transactional_db'):
            return 1

        return 0

    items.sort(key=weight_test_case)
