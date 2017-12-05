"""
"""
from django.shortcuts import render
from django.views.generic.base import TemplateView


class MyAppView(TemplateView):
    template_name = 'myapp.html'

    def get_context_data(self, **kwargs):
        return {'key': 'value'}
