from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from services.views import ServiceViewset, CategoryViewset, ServiceReviewViewset
from orders.views import OrderViewSet
from dashboard import views
router = DefaultRouter()
#Main Routers
router.register('services', ServiceViewset, basename='services')
router.register('categories',CategoryViewset, basename='categories')
router.register('orders', OrderViewSet, basename='orders')
router.register("seller/dashboard", views.SellerDashboardViewSet, basename="seller-dashboard")
router.register("seller/profile", views.SellerProfileViewSet, basename="seller-profile")
router.register("seller/services", views.SellerServiceViewSet, basename="seller-services")
router.register("buyer/dashboard", views.BuyerDashboardViewSet, basename="buyer-dashboard")

#Nested Routers
services_router = routers.NestedDefaultRouter(router, 'services', lookup='service')
services_router.register('reviews', ServiceReviewViewset, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(services_router.urls)),
]