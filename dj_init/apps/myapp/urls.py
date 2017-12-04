"""
"""
from django.conf.urls import include, url

from dj_init.apps.myapp import views


urlpatterns = [
    # admin urls
    url(r'^$', views.MyAppView.as_view(), name='web-home'),
]
