from django_filters.rest_framework import FilterSet
from services.models import Service
class ServiceFilter(FilterSet):
    class Meta:
        model = Service
        fields = {
            'category_id': ['exact'],
            'price': ['lt', 'gt']
        }