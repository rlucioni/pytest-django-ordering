pytest-django-ordering |PyPI|_ |Travis|_
========================================
.. |PyPI| image:: https://img.shields.io/pypi/v/pytest-django-ordering.svg?style=flat-square&maxAge=3600
.. _PyPI: https://pypi.python.org/pypi/pytest-django-ordering

.. |Travis| image:: https://img.shields.io/travis/rlucioni/pytest-django-ordering.svg?style=flat-square&maxAge=3600
.. _Travis: https://travis-ci.org/rlucioni/pytest-django-ordering

`pytest-django`_ advertises "easy switching." While it's true that existing unittest-style
tests will work without any modifications, you may have problems switching if you
depend on the `order`_ in which the Django test runner runs tests. This plugin helps
preserve that order if you need it to run your tests.

.. _pytest-django: https://pytest-django.readthedocs.io/en/latest/
.. _order: https://docs.djangoproject.com/en/dev/topics/testing/overview/#order-in-which-tests-are-executed

Motivation
----------

The Django test runner gives priority to Django ``TestCase`` subclasses, executing them
before other Django-based tests (e.g., ``TransactionTestCase``) and any other ``unittest.TestCase``
tests. Put differently, Django runs tests which reset the database by rolling back
a transaction before tests which reset the database by truncating all tables.

pytest-django doesn't preserve this ordering out of the box. For more, see `#214`_.
This isn't a problem if your project's tests can run independently of each other,
in any order. However, if your project's tests rely on initial data populated via
fixtures or migrations, tests which reset the database by rolling back a transaction
*must* run before tests which reset the database by truncating all tables, thereby
deleting any initial data. The ``serialized_rollback`` option can be used to deal with
this issue within a ``TransactionTestCase``, but it has no effect across distinct
test cases; once you exit a ``TransactionTestCase``, any initial data is gone.

.. _#214: https://github.com/pytest-dev/pytest-django/issues/214

Installation
------------

This plugin supports Python 2.7, 3.5, and 3.6. Install with ``pip``::

    $ pip install pytest-django-ordering

You're done! ``pytest`` will automatically find and integrate the plugin.
