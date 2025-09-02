from django.shortcuts import render
from rest_framework import viewsets, permissions
from orders.models import Order
from orders.serializers import OrderSerializer
from services.models import Service

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        service = serializer.validated_data['service']
        serializer.save(
            buyer=self.request.user,
            seller=service.seller
        )

    def get_queryset(self):
        user = self.request.user
        if user.role == "BUYER":
            return Order.objects.filter(buyer=user)
        elif user.role == "SELLER":
            return Order.objects.filter(seller=user)
        return Order.objects.none()
