"""
"""
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from dj_init.apps.myapp import api_views

router = DefaultRouter()
urlpatterns = router.urls


urlpatterns += [
    url(r'^myapi/$', api_views.MyAppView.as_view(), name='my-app-api'),
]
