"""
Force import of all modules in this package in order to get the standard test
runner to pick up the tests.  Yowzers.
"""
from __future__ import unicode_literals, print_function
import os
import traceback
import django

modules = [filename.rsplit('.', 1)[0]
           for filename in os.listdir(os.path.dirname(__file__))
           if filename.endswith('.py') and not filename.startswith('_')]
__test__ = dict()

if django.VERSION < (1, 6):
    for module in modules:
        print('loading module %-20s' % module, end='')
        try:
            exec("from django_services.tests.%s import *" % module)
            print('ok')
        except:
            print('error\n%s' % traceback.format_exc())
            raise


