from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from users.views import UserViewSet
router = DefaultRouter()
router.register('authors', AuthorViewSet, basename='author')
router.register('books', BookViewSet, basename='book')
router.register('members', MemberViewSet, basename='member')
router.register('borrow-records', BorrowRecordViewSet, basename='borrow-record')
router.register('users',UserViewSet, basename='users')
urlpatterns = router.urls
