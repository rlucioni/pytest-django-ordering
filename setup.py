from setuptools import setup


with open('README.rst') as readme:
    long_description = readme.read()


setup(
    name='pytest-django-ordering',
    version='1.2.0',
    description='A pytest plugin for preserving the order in which Django runs tests.',
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'Framework :: Pytest',
    ],
    url='https://github.com/rlucioni/pytest-django-ordering',
    author='Renzo Lucioni',
    author_email='renzo@lucioni.xyz',
    license='MIT',
    install_requires=['django', 'pytest>=2.3.0', 'pytest-django'],
    packages=['pytest_django_ordering'],
    entry_points={
        'pytest11': [
            'django_ordering = pytest_django_ordering.plugin',
        ]
    },
)
