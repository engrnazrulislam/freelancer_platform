from decimal import Decimal
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from services.models import Service, ServiceReview
from orders.models import Order
from dashboard import serializers
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# Seller Dashboard
class SellerDashboardViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.SellerServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(seller=self.request.user)

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        seller = request.user
        services = Service.objects.filter(seller=seller)
        orders = Order.objects.filter(seller=seller)
        completed_orders = orders.filter(status=Order.COMPLETED)
        reviews = ServiceReview.objects.filter(service__seller=seller)

        total_earnings = completed_orders.aggregate(
            total=Sum("service__price")
        )["total"] or Decimal("0")

        data = {
                "total_services": services.count(),
                "total_orders": orders.count(),
                "completed_orders": completed_orders.count(),
                "total_earnings": total_earnings,
                "services": services,
                "orders": orders,
                "reviews": reviews,
            }

        serializer = serializers.SellerDashboardSerializer(data)
        return Response(serializer.data)

# Seller Profile
class SellerProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user



# Buyer Dashboard

class BuyerDashboardViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.BuyerOrderSerializer

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        buyer = request.user
        orders = Order.objects.filter(buyer=buyer)
        completed_orders = orders.filter(status=Order.COMPLETED)
        reviews = buyer.buyer_reviews.all()

        total_spent = completed_orders.aggregate(
            total=Sum("service__price")
        )["total"] or Decimal("0")

        data = {
            "total_orders": orders.count(),
            "completed_orders": completed_orders.count(),
            "total_spent": total_spent,
            "orders": orders,
            "reviews": reviews,
        }
        serializer = serializers.BuyerDashboardSerializer(data)
        return Response(serializer.data)


# Buyer Profile
class BuyerProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user
