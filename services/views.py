from django.shortcuts import render
from rest_framework import viewsets
from services.models import Service, Category, ServiceReview
from services.serializers import ServiceSerializer, CategorySerializer, ServiceDetailSerializer, ServiceReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from services.filters import ServiceFilter
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class ServiceViewset(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['title','description','category__name']
    ordering_fields = ['price']

    def get_queryset(self):
        return Service.objects.filter(is_active=True).all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceDetailSerializer
        return ServiceSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ServiceReviewViewset(viewsets.ModelViewSet):
    serializer_class = ServiceReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ServiceReview.objects.filter(service_id=self.kwargs['service_pk'])
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user, service_id=self.kwargs['service_pk'])

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
