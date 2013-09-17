from django_services.api import DjangoServiceSerializer
from .models import Brand

class BrandSerializer(DjangoServiceSerializer):

    class Meta:
        model = Brand
        fields = ('name',)
