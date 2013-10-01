from django.contrib import admin
from django_services import admin as django_services_admin
from .models import Brand, Model, Car
from .service import BrandService, ModelService, CarService

class BrandAdmin(django_services_admin.DjangoServicesAdmin):
    service_class = BrandService

class ModelAdmin(django_services_admin.DjangoServicesAdmin):
    service_class = ModelService

class CarAdmin(django_services_admin.DjangoServicesAdmin):
    service_class = CarService

admin.site.register(Brand, BrandAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Car, CarAdmin)
