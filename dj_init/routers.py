"""
"""
from django.conf import settings
from django.conf.urls import include, url

from dj_init.views import api_root


urlpatterns = [
    url(r'^$', api_root, name='api_root'),
    url(r'^', include('dj_init.apps.myapp.routers')),
]
