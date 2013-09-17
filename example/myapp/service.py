from django_services import service
from .models import Brand, Model, Car

class BrandService(service.CRUDService):
    model_class = Brand


class ModelService(service.CRUDService):
    model_class = Model


class CarService(service.CRUDService):
    model_class = Car
