from rest_framework import serializers
from orders.models import Order
from services.models import Service, ServiceReview

class SellerServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "title", "description", "price", "delivery_time", "is_active", "category"]

class SellerReviewSerializer(serializers.ModelSerializer):
    buyer_email = serializers.CharField(source="buyer.email", read_only=True)
    service_title = serializers.CharField(source="service.title", read_only=True)

    class Meta:
        model = ServiceReview
        fields = ["id", "service_title", "rating", "review", "buyer_email"]

class BuyerOrderSerializer(serializers.ModelSerializer):
    service_title = serializers.CharField(source="service.title", read_only=True)
    service_price = serializers.DecimalField(source="service.price", max_digits=10, decimal_places=2, read_only=True)
    seller_email = serializers.CharField(source="seller.email", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "service_title", "service_price", "seller_email", "status"]

class BuyerReviewSerializer(serializers.ModelSerializer):
    service_title = serializers.CharField(source="service.title", read_only=True)

    class Meta:
        model = ServiceReview
        fields = ["id", "service_title", "rating", "review"]