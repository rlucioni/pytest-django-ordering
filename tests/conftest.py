import shutil
from textwrap import dedent

import py
import pytest

# Makes the testdir fixture available.
pytest_plugins = 'pytester'

REPOSITORY_ROOT = py.path.local(__file__).join('..')


@pytest.fixture(scope='function')
def django_testdir(request, testdir, monkeypatch):
    # Create a Django project.
    project_root = testdir.tmpdir
    project_root.ensure('manage.py')

    # Create an app in the Django project.
    app_source = REPOSITORY_ROOT.dirpath('tests/app')
    test_app_path = project_root.join('app')
    shutil.copytree(
        py.builtin._totext(app_source),
        py.builtin._totext(test_app_path)
    )

    monkeypatch.setenv('DJANGO_SETTINGS_MODULE', 'app.settings')

    def create_test_module(test_code, filename='test_stuff.py'):
        f = test_app_path.join(filename)
        f.write(dedent(test_code), ensure=True)
        return f

    testdir.create_test_module = create_test_module
    testdir.project_root = project_root

    return testdir
