from django_services.api import DjangoServiceAPI, register
from .models import Brand, Model, Car
from .service import BrandService, CarService, ModelService
from .serializers import BrandSerializer, CarSerializer, ModelSerializer

class CarAPI(DjangoServiceAPI):
    serializer_class = CarSerializer
    service_class = CarService

class ModelAPI(DjangoServiceAPI):
    serializer_class = ModelSerializer
    service_class = ModelService
    
class BrandAPI(DjangoServiceAPI):
    """
    *   ### __List Virtual Machines__
    
        __GET__ /api/virtualmachine/
    
    *   ### __To create a new virtual machine on a virtual group__
    
        __POST__ /api/virtualmachine/
    
            {
                "virtual_group": "{api_url}/virtualgroup/{vg_id}/"
            }
    
    *   ### __Show details about a Virtual Machine__
    
        __GET__ /api/virtualmachine/`vm_id`/
    
        __GET__ /api/virtualmachine/`description`/
    
    *   ### __To delete a Virutal Machine:__
    
        __DELETE__ /api/virtualmachine/`vm_id`/
    
    *   ### __To start or stop a Virtual Machine:__
    
        __PUT__ /api/virtualmachine/`vm_id`/
    
            {
                "state": "start|stop"
            }
    
    """
    serializer_class = BrandSerializer
    service_class = BrandService
    filter_fields = ('description', 'virtual_group', 'host')
    operations = ('list', 'retrieve', 'create', 'update', 'destroy')


register('brand', BrandAPI)
register('car', CarAPI)
register('model', ModelAPI)