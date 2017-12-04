"""
custom generic filter backend
"""
# from rest_framework import filters ## For rest_framework < 3.5
from django_filters import rest_framework


class ModifiedAtFilterBackend(rest_framework.DjangoFilterBackend):
    """
    """
    def filter_queryset(self, request, queryset, view):

        if 'modified_at_gt' in  request.query_params:
            queryset = queryset.filter(modified_at__gt=request.query_params['modified_at_gt'])

        if 'modified_at_lt' in  request.query_params:
            queryset = queryset.filter(modified_at__lt=request.query_params['modified_at_lt'])
        return queryset


class CreatedAtFilterBackend(rest_framework.DjangoFilterBackend):
    """
    """
    def filter_queryset(self, request, queryset, view):

        if 'created_at_gt' in  request.query_params:
            queryset = queryset.filter(created_at__gt=request.query_params['created_at_gt'])

        if 'created_at_lt' in  request.query_params:
            queryset = queryset.filter(created_at__lt=request.query_params['created_at_lt'])
        return queryset
