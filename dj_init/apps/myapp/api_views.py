"""
"""
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route, parser_classes
from rest_framework import permissions, status, viewsets, filters, parsers

User = get_user_model()


class MyAppView(APIView):
    """
    """
    def get(self, request, format=None):
        response = {"detail": "success"}
        return Response(response, status=status.HTTP_200_OK)
