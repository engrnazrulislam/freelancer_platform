from django.shortcuts import render
from rest_framework import viewsets, permissions
from services.models import Service, Category, ServiceReview, ServiceImage
from services.serializers import ServiceSerializer, CategorySerializer, ServiceDetailSerializer, ServiceReviewSerializer, ServiceImageSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from services.filters import ServiceFilter
from rest_framework.decorators import action
from services.serializers import ServiceSerializer, ServiceDetailSerializer
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class SellerServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(seller=self.request.user)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ServiceDetailSerializer
        return ServiceSerializer
    
    @swagger_auto_schema(
        operation_summary="List seller's services",
        operation_description="Retrieve all services created by the logged-in seller"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new service",
        request_body=ServiceSerializer,
        responses={201: ServiceSerializer, 400: "Bad Request"}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class SellerServiceImageViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceImage.objects.filter(
            service__seller=self.request.user,
            service_id=self.kwargs["service_pk"]
        )

    def perform_create(self, serializer):
        serializer.save(service_id=self.kwargs["service_pk"])
    
    @swagger_auto_schema(
        operation_summary="List images for seller's service"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class SellerServiceReviewViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ServiceReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceReview.objects.filter(
            service__seller=self.request.user,
            service_id=self.kwargs["service_pk"]
        )

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['title','description','category__name']
    ordering_fields = ['price']

    def get_queryset(self):
        return Service.objects.filter(is_active=True).select_related('category','seller').prefetch_related('images','service_reviews')

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ServiceDetailSerializer
        return ServiceSerializer
    @swagger_auto_schema(
        operation_summary="List all active services",
        operation_description="Public API: anyone can see active services. Supports filter, search, ordering."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a service",
        operation_description="Get detailed info about a single service"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
class ServiceReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceReview.objects.filter(service_id=self.kwargs['service_pk'])

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

    def perform_update(self, serializer):
        serializer.save(buyer=self.request.user)

    @swagger_auto_schema(
    operation_summary="List reviews for a service"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Add a review for a service",
        request_body=ServiceReviewSerializer,
        responses={201: ServiceReviewSerializer, 400: "Bad Request"}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class ServiceImageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ServiceImageSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return ServiceImage.objects.filter(service__is_active=True)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    @swagger_auto_schema(
        operation_summary="List reviews for a service"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Add a review for a service",
        request_body=ServiceReviewSerializer,
        responses={201: ServiceReviewSerializer, 400: "Bad Request"}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
