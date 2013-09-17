import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

STATUS_PROD = 'Development Status :: 5 - Production/Stable'
STATUS_BETA = 'Development Status :: 4 - Beta'
STATUS_ALPHA = 'Development Status :: 3 - Alpha'

version = '0.0.3'
README = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(README).read()


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


setup(
    name='django-services',
    version=version,
    description="Django Services Pattern Support",
    long_description=long_description,
    classifiers=[
        STATUS_PROD,
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'],
    keywords='django model admin rest api service',
    author='Silvano Buback',
    author_email='snbuback@gmail.com',
    url='https://github.com/snbuback/django-services',
    license='APACHE2',
    packages=find_packages('.', exclude=('testproject*',)),
    include_package_data=True,
    require=['Django', 'mock', 'djangorestframework'],
    tests_require=['tox'],
    cmdclass = {'test': Tox},
)
