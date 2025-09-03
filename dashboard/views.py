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

class SellerDashboardViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SellerServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(seller=self.request.user)

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        seller = request.user
        services = Service.objects.filter(seller=seller)
        orders = Order.objects.filter(seller=seller)
        completed_orders = orders.filter(status=Order.COMPLETED)
        earnings = calculate_earnings(completed_orders)
        reviews = ServiceReview.objects.filter(service__seller=seller)

        def calculate_earnings(orders_queryset):
            result = orders_queryset.aggregate(Sum("service__price"))
            total = result.get("service__price__sum")
            if total is None:
                return Decimal("0")
            return total

        data = {
            "total_services": services.count(),
            "total_orders": orders.count(),
            "completed_orders": completed_orders.count(),
            "total_earnings": earnings,
            "services": serializers.SellerServiceSerializer(services, many=True).data,
            "orders": [
                {
                    "id": str(order.id),
                    "service": order.service.title,
                    "buyer": order.buyer.email,
                    "status": order.status,
                } for order in orders
            ],
            "reviews": [
                {
                    "id": str(review.id),
                    "service": review.service.title,
                    "rating": review.rating,
                    "review": review.review,
                    "buyer": review.buyer.email,
                } for review in reviews
            ],
        }
        return Response(data)

class SellerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user


class SellerServiceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SellerServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(seller=self.request.user)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
#Buyer Section
class BuyerDashboardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BuyerOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        buyer = request.user
        orders = Order.objects.filter(buyer=buyer)
        completed_orders = orders.filter(status=Order.COMPLETED)
        spent = calculate_total_spent(completed_orders)
        reviews = buyer.buyer_reviews.all()

        def calculate_total_spent(orders_queryset):
            result = orders_queryset.aggregate(Sum("service__price"))
            total = result.get("service__price__sum")
            if total is None:
                return Decimal("0")
            return total

        data = {
            "total_orders": orders.count(),
            "completed_orders": completed_orders.count(),
            "total_spent": spent,
            "orders": [
                {
                    "id": str(order.id),
                    "service": order.service.title,
                    "seller": order.seller.email,
                    "status": order.status,
                    "price": order.service.price,
                } for order in orders
            ],
            "reviews": [
                {
                    "id": str(review.id),
                    "service": review.service.title,
                    "rating": review.rating,
                    "review": review.review,
                } for review in reviews
            ],
        }
        return Response(data)
