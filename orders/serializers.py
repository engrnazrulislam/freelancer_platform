from rest_framework import serializers
from orders.models import Order
class OrderSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source="buyer.first_name", read_only=True)
    seller_name = serializers.CharField(source="seller.first_name", read_only=True)
    service_title = serializers.CharField(source="service.title", read_only=True)
    class Meta:
        model = Order
        fields = [
            'id', 'buyer', 'buyer_name', 'seller', 'seller_name',
            'service', 'service_title', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['buyer', 'seller', 'status']