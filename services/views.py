from django.shortcuts import render
from rest_framework import viewsets
from services.models import Service
from services.serializers import ServiceSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from services.filters import ServiceFilter
# Create your views here.
class ServiceViewset(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['category__name']
    ordering_fields = ['price']

    def get_queryset(self):
        return Service.objects.prefetch_related('category_services').filter(is_active=True).all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)