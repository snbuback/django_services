django-services
===============

A small api integrated to django rest framework (http://django-rest-framework.org/) that makes django admin and all api's calls share the same logic. 

For instance, if you save a object using django's admin or the api the same logic will be used.

**requires python >= 2.7**

Running local
--------------

Create a virtualenv environment

    mkvirtualenv --python=python2.7 django_services
    workon django_services

In order to run this project local or to run its tests, you need to run _make pip_ to install all the dependencies

Usage
-----

Basically, you need to inherit admin.DjangoServicesAdmin class in your admin class

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

Then you have to follow django rest framework conventions to create your api.

Check the example app!

Changelog
---------

* 0.0.8
    * overrides django admin's delete_selected action to use service delete
    * improves example app
    * documentation
    * creates requirements file for testing and running the example app


contributing
------------

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request =]