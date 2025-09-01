from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework_nested import routers
# from users.views import UserViewSet
from services.views import ServiceViewset
router = DefaultRouter()
router.register('services', ServiceViewset, basename='services')
urlpatterns = router.urls
