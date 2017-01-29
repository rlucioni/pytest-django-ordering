from django.test import TestCase


def pytest_collection_modifyitems(items):
    def is_testcase_subclass(test):
        """
        The default Django test runner gives priority to TestCase subclasses,
        executing them before all Django-based tests (e.g., TransactionTestCase)
        and any other unittest.TestCase tests; see
        https://docs.djangoproject.com/en/1.9/topics/testing/overview/#order-in-which-tests-are-executed.

        pytest-django doesn't preserve this ordering out of the box. For more on
        this, see https://github.com/pytest-dev/pytest-django/issues/214.

        This isn't a problem if your project's tests can run independently of each
        other, in any order. Sadly, the majority of this project's tests rely on
        initial data populated via migrations, which means that TestCase subclasses
        *must* run before TransactionTestCase subclasses which reset the database
        by truncating all tables, deleting any initial data. (The serialized_rollback
        option can be used to remedy this within a given TransactionTestCase, but
        it has no effect across distinct test cases; once you exit a TransactionTestCase,
        any intial data is gone.)
        """
        # TODO: False (0) sorts before True (1).
        if test.cls and issubclass(test.cls, TestCase):
            return 0

        return 1

    items.sort(key=is_testcase_subclass)
