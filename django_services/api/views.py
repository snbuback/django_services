# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.core.urlresolvers import reverse
from ..api import router
from .utils import get_view_doc


def api_help(request):
    breadcrumblist = [
        ('API Help', '/api'),
    ]

    # iterate over all registered apis
    api_doc_list = []
    for prefix, viewset, basename in router.registry:
        api_doc = APIDoc(viewset=viewset, basename=basename)
        api_doc_list.append(api_doc)

    # order by name
    api_doc_list.sort()

    return render(request, 'api_help.html', {
        "breadcrumblist": breadcrumblist,
        "api_doc_list": api_doc_list,
        "request": request,
    }, content_type="text/html")


class APIDoc(object):

    def __init__(self, viewset, basename):
        self.viewset = viewset
        self.basename = basename

    @property
    def name(self):
        return self.basename

    @property
    def view_name(self):
        list_name_prefix = router.routes[0].name
        view_name = list_name_prefix.format(basename=self.basename)
        return view_name

    @property
    def url(self):
        return reverse(self.view_name)

    @property
    def documentation(self):
        return get_view_doc(self.viewset)

    def __cmp__(self, other):
        if self.name == other.name:
            return 0
        elif self.name > other.name:
            return 1
        return -1
