# -*- coding:utf-8 -*-

import logging
import os.path
from importlib import import_module
from django.conf import settings
from django.conf.urls import patterns, url, include
from . import router

LOG = logging.getLogger(__name__)


for app in settings.INSTALLED_APPS:
    try:
        base_module = import_module(app)
        import_module("%s.api" % app)
        # load all api.py application modules
    except ImportError, e:
        if os.path.exists(os.path.abspath(os.path.join(base_module.__file__, '../api.py'))):
            # File exists, error on import
            raise

urlpatterns = patterns(
    'django_services.api.views',
    url(r'^$', 'api_help', name='api.index'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
