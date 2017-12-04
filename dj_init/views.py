"""
"""
from collections import OrderedDict

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    """
    Each API Endpoint contains corresponding documentation.
    """
    return Response(OrderedDict([
        # Influencer apis listing
        ('dj_init', OrderedDict([
            ('myapp-api', reverse('my-app-api', request=request, format=format)),
        ])),
    ]))
