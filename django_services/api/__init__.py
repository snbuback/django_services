# -*- coding:utf-8 -*-

import logging
from rest_framework.routers import SimpleRouter
from .serializers import DjangoServiceSerializer
from .api import DjangoServiceAPI, exception_translation

router = SimpleRouter()
LOG = logging.getLogger(__name__)

__all__ = ['DjangoServiceSerializer', 'DjangoServiceAPI', 'exception_translation', 'register']


def register(name, viewsets, *args):
    router.register(name, viewsets, *args)
    LOG.debug(u'Registered api %s with viewset %s', name, viewsets)
