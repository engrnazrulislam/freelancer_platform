from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
# from users.views import UserViewSet
from services.views import ServiceViewset, CategoryViewset, ServiceReviewViewset
router = DefaultRouter()
router.register('services', ServiceViewset, basename='services')
router.register('categories',CategoryViewset, basename='categories')

services_router = routers.NestedDefaultRouter(router, 'services', lookup='service')
services_router.register('reviews', ServiceReviewViewset, basename='reviews')

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(services_router.urls))
]