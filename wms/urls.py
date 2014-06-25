from django.conf.urls import patterns, url
from .views import wms

urlpatterns = patterns('',
    url(r'^$', wms, name='wms'),
)
