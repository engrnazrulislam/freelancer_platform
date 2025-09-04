from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from services.views import (
    ServiceViewSet, 
    CategoryViewSet, 
    ServiceReviewViewSet, 
    ServiceImageViewSet,
    SellerServiceViewSet, 
    SellerServiceImageViewSet, 
    SellerServiceReviewViewSet,
    )
from dashboard.views import (
    SellerDashboardViewSet,
    BuyerDashboardViewSet,
    SellerProfileViewSet,
    BuyerProfileViewSet,
)
from orders.views import OrderViewSet
router = DefaultRouter()
#General Routers
router.register('services', ServiceViewSet, basename='services')
router.register('categories',CategoryViewSet, basename='categories')
router.register('orders', OrderViewSet, basename='orders')
#Seller Routers
router.register("seller/dashboard", SellerDashboardViewSet, basename="seller-dashboard")
router.register("seller/profile", SellerProfileViewSet, basename="seller-profile")
router.register("seller/services", SellerServiceViewSet, basename="seller-services")
# Buyer Routers
router.register("buyer/dashboard", BuyerDashboardViewSet, basename="buyer-dashboard")
router.register("buyer/profile", BuyerProfileViewSet, basename="buyer-profile")
#Nested General Routers
services_router = routers.NestedDefaultRouter(router, 'services', lookup='service')
services_router.register('reviews', ServiceReviewViewSet, basename='reviews')
services_router.register('images', ServiceImageViewSet, basename='service-images')
#Seller Nested Seller Routes
seller_services_router = routers.NestedDefaultRouter(router, "seller/services", lookup="service")
seller_services_router.register("images", SellerServiceImageViewSet, basename="seller-service-images")
seller_services_router.register("reviews", SellerServiceReviewViewSet, basename="seller-service-reviews")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(services_router.urls)),
    path('', include(seller_services_router.urls))
]