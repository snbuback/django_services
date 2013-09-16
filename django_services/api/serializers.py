# -*- coding:utf-8 -*-

from rest_framework import serializers


class DjangoServiceSerializer(serializers.HyperlinkedModelSerializer):
    """
    Base class for DjangoService API serializers.
    """
