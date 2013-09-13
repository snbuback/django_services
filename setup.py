import os
from setuptools import setup, find_packages

STATUS_PROD = 'Development Status :: 5 - Production/Stable'
STATUS_BETA = 'Development Status :: 4 - Beta'
STATUS_ALPHA = 'Development Status :: 3 - Alpha'

version = '0.0.1'
README = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(README).read()
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
        'License :: OSI Approved :: Apache2 License',
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
)
