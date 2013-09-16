# -*- coding:utf-8 -*-

import logging
import json
from functools import wraps
from django.http import Http404
from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response
from .exceptions import InvalidOperationException

LIST = 'list'
CREATE = 'create'
RETRIEVE = 'retrieve'
UPDATE = 'update'
DESTROY = 'destroy'
DEFAULT_OPERATIONS = frozenset([LIST, RETRIEVE])
ALL_OPERATIONS = frozenset([LIST, CREATE, RETRIEVE, UPDATE, DESTROY])

LOG = logging.getLogger(__name__)


def make_json(detail):
    return json.dumps({'detail': detail})


def exception_translation(func):
    """
    Catch exception and build correct api response for it.
    """
    @wraps(func)
    def decorator(*arg, **kwargs):
        try:
            return func(*arg, **kwargs)
        except InvalidOperationException, e:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED, data={'detail': e.message}, headers={'Content-Type': 'application/json'})
    return decorator


def getattr_in_cls_list(cls_list, attr, default):
    """ Search for an attribute (attr) in class list (cls_list). Returns
    attribute value if exists or None if not. """
    for cls in cls_list:
        if hasattr(cls, attr):
            return getattr(cls, attr)
    return default


class create_api_class(type):
    def __new__(mcs, name, bases, attrs):

        if name == 'DjangoServiceAPI':
            # use default class creator
            return type.__new__(mcs, name, bases, attrs)

        new_bases = list(bases)

        # remove object class
        if object in new_bases:
            new_bases.remove(object)

        if not 'model' in attrs:
            attrs['model'] = attrs['service_class'].model_class

        # extract operations attribute. Try to search subclasses
        if 'operations' in attrs:
            operations = attrs['operations']
        else:
            operations = getattr_in_cls_list(new_bases, 'operations', DEFAULT_OPERATIONS)

        # verify if all operations are known.
        if not ALL_OPERATIONS.issuperset(operations):
            raise RuntimeError("Invalid operations: %s in %s" % (list(set(operations) - ALL_OPERATIONS), name))

        if LIST in operations:
            new_bases.append(mixins.ListModelMixin)

        if CREATE in operations:
            new_bases.append(CreateModelUsingService)

        if RETRIEVE in operations:
            new_bases.append(mixins.RetrieveModelMixin)

        if UPDATE in operations:
            new_bases.append(UpdateModelUsingService)

        if DESTROY in operations:
            new_bases.append(DestroyModelUsingService)

        new_bases += (generics.SingleObjectAPIView, generics.MultipleObjectAPIView,)

        return type.__new__(mcs, name, tuple(new_bases), attrs)


class DestroyModelUsingService(mixins.DestroyModelMixin):
    """
    Use service model to call destroy
    """
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.service.delete(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateModelUsingService(mixins.CreateModelMixin):
    """
    Use service model to call create
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = self.service.create(serializer.object)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateModelUsingService(mixins.UpdateModelMixin):
    """
    Use service model to call update
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        self.object = self.get_object()
        serializer = self.get_serializer(self.object, data=request.DATA,
                                         files=request.FILES, partial=partial)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = self.service.update(self.object)
            self.post_save(self.object, created=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DjangoServiceAPI(viewsets.GenericViewSet):
    __metaclass__ = create_api_class

    @property
    def http_request(self):
        return self.request._request

    @property
    def user(self):
        return self.http_request and self.http_request.user

    @property
    def service(self):
        '''
        Instantiate service class with django http_request
        '''
        service_class = getattr(self, 'service_class')
        service = service_class(self.http_request)
        return service

    def get_queryset(self):
        # allow serializer without service
        query = self.service.list()
        return query

    def get_object(self, queryset=None):
        """
        Override default to add support for object-level permissions.
        """
        try:
            pk = self.kwargs.get('pk', None)

            # allow serializer without service
            obj = self.service.get(pk)
            return obj
        except self.model.DoesNotExist:
            raise Http404()

    def response_object(self, obj, status=status.HTTP_200_OK):
        serializer = self.get_serializer(instance=obj)
        return Response(serializer.data, status=status)
