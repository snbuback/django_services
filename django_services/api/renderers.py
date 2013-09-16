# -*- coding:utf-8 -*-

import logging
from rest_framework import renderers
from django.conf import settings
from .utils import wrap_accordion, get_view_doc

LOG = logging.getLogger(__name__)


class CustomBrowsableAPIRenderer(renderers.BrowsableAPIRenderer):

    def get_description(self, view):

        view_doc = get_view_doc(view)
        # convert to html
        description = wrap_accordion([('Documentation', view_doc)])
        return description

    def show_form_for_method(self, view, method, request, obj):
        if not getattr(settings, 'ALLOW_API_BROWSER_USE_CHANGING_METHODS', True) and not (method in ['GET', 'OPTIONS']):
            LOG.debug("Browser render don't allow changing methods")
            return False

        return super(CustomBrowsableAPIRenderer, self).show_form_for_method(view, method, request, obj)
