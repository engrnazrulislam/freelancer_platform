from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orders.models import Order
from orders.serializers import OrderSerializer
from drf_yasg.utils import swagger_auto_schema


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_user_role(self):
        """Return user role in uppercase (BUYER, SELLER, ADMIN)."""
        return getattr(self.request.user, "role", "").upper()

    def get_queryset(self):
        """Return queryset filtered by role:
        - Admin → All orders
        - Buyer → Own orders
        - Seller → Orders related to their services
        """
        user = self.request.user
        role = getattr(user, "role", "").upper()

        qs = Order.objects.all().select_related("buyer","seller","service")

        if user.is_staff or role == "ADMIN":
            return qs
        if role == "BUYER":
            return qs.filter(buyer=user)
        if role == "SELLER":
            return qs.filter(seller=user)
        return Order.objects.none()

    def can_user_modify_order(self, order):
        """Return allowed actions for this user"""
        role = self.get_user_role()
        user = self.request.user
        return {
            "is_buyer": role=="BUYER" and order.buyer==user,
            "is_seller": role=="SELLER" and order.seller==user,
            "is_admin": role=="ADMIN" or user.is_staff
        }
    @swagger_auto_schema(
    operation_summary="List orders",
    operation_description=(
        "Admin → can view all orders.\n"
        "Buyer → can view only their orders.\n"
        "Seller → can view orders related to their services."
    ),
    responses={200: OrderSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        role = self.get_user_role()
        user = self.request.user
        if role in ["BUYER","ADMIN"] or user.is_staff:
            serializer.save(
                buyer=user,
                seller=serializer.validated_data["service"].seller
            )
        else:
            raise serializers.ValidationError("Only buyers and admins can place orders.")

    def partial_update(self, request, *args, **kwargs):
        """Check if user can modify the given order based on role."""
        order = self.get_object()
        user_actions = self.can_user_modify_order(order)
        new_status = request.data.get("status")
        allowed_status = ['PENDING','APPROVED','CANCELLED','COMPLETED']

        if new_status not in allowed_status:
            return Response({'error':'Invalid status'}, status=400)

        # Buyer can cancel
        if user_actions["is_buyer"]:
            if new_status=="CANCELLED":
                order.status = new_status
                order.save()
                return Response(self.get_serializer(order).data)
            return Response({'error':'Buyer can only cancel'}, status=403)

        # Seller can update
        if user_actions["is_seller"] or user_actions["is_admin"]:
            order.status = new_status
            order.save()
            return Response(self.get_serializer(order).data)

        return Response({'error':'Permission denied'}, status=403)