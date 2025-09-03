from rest_framework import serializers
from orders.models import Order

class OrderSerializer(serializers.ModelSerializer):
    buyer_name = serializers.SerializerMethodField(method_name='get_buyer_name')
    seller_name = serializers.SerializerMethodField(method_name='get_seller_name')
    service_title = serializers.SerializerMethodField(method_name='get_service_title')
    class Meta:
        model = Order
        fields = [
            'id', 'buyer', 'buyer_name', 'seller', 'seller_name',
            'service', 'service_title', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['buyer', 'seller', 'status']
    
    def get_buyer_name(self, obj):
            if obj.buyer:
                return obj.buyer.get_full_name() or obj.buyer.email
            return None

    def get_seller_name(self, obj):
            if obj.seller:
                return obj.seller.get_full_name() or obj.seller.email
            return None

    def get_service_title(self, obj):
            if obj.service:
                return obj.service.title
            return None