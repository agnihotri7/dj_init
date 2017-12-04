"""
"""
from django.conf import settings


def my_custom_processor(request):
    return {'my_key': "my_value"}
