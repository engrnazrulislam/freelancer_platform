from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from orders.models import Order
from orders.serializers import OrderSerializer
from rest_framework import serializers
# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        service = serializer.validated_data['service']
        user = self.request.user
        role = getattr(user, "role", "").upper() 

        if role == "BUYER":
            serializer.save(
                buyer=user,
                seller=service.seller
            )
        elif role == "ADMIN" or user.is_staff:
            serializer.save(
                buyer=user,
                seller=service.seller
            )
        else:
            raise serializers.ValidationError("Only buyers and admins can place orders.")

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, "role", "").upper()

        if user.is_staff or role == "ADMIN":
            return Order.objects.all()
        if role == "BUYER":
            return Order.objects.filter(buyer=user)
        if role == "SELLER":
            return Order.objects.filter(seller=user)
        return Order.objects.none()

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        if request.user != order.seller and not request.user.is_superuser:
            return Response({'error': 'Permission denied'}, status=403)

        new_status = request.data.get('status')
        if new_status not in ['PENDING', 'APPROVED', 'CANCELLED']:
            return Response({'error': 'Invalid status'}, status=400)

        order.status = new_status
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        if not request.user.is_superuser:
            return Response({'error': 'Only admin can delete'}, status=403)
        order.delete()
        return Response({'success': 'Order deleted'})

