from django_services.api import DjangoServiceSerializer
from .models import Brand, Car, Model

class BrandSerializer(DjangoServiceSerializer):

    class Meta:
        model = Brand
        fields = ('name',)

class ModelSerializer(DjangoServiceSerializer):

    class Meta:
        model = Model
        fields = ('name', 'brand')

class CarSerializer(DjangoServiceSerializer):

    class Meta:
        model = Car
        fields = ('model', 'year')