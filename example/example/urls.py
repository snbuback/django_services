from django.conf.urls import patterns, include, url
import django_services.api.urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '', 
    url('^admin/', include(admin.site.urls)),
    url('^api/', include(django_services.api.urls))
)
