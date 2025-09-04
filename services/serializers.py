from rest_framework import serializers
from services.models import Service, Category, ServiceReview, ServiceImage
from django.contrib.auth import get_user_model
User = get_user_model()

class SimpleUserSerializer(serializers.ModelSerializer):
    name  = serializers.SerializerMethodField(method_name='get_current_user_name')
    class Meta:
        model = User
        fields = ['id','name']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ServiceImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ServiceImage
        fields = ['id','image']

class ServiceSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)
    class Meta:
        model = Service
        fields = ['id','seller','title','description','images','price','category','created_at','updated_at','delivery_time']
        read_only_fields = ['seller','created_at','updated_at']

class ServiceReviewSerializer(serializers.ModelSerializer):
    buyer_name = serializers.SerializerMethodField(method_name='get_buyer')
    class Meta:
        model = ServiceReview
        fields = ['id','buyer','buyer_name','rating','review','created_at']
        read_only_fields = ['buyer', 'created_at']

        def get_buyer(self, obj):
            if obj.buyer:
                return obj.buyer.get_full_name() or obj.buyer.email
            return None
        
        def create(self, validated_data):
            service_id = self.context['service_id']
            review = ServiceReview.objects.create(service_id=service_id, **validated_data)
            return review

class ServiceDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    reviews = ServiceReviewSerializer(many=True, read_only=True)
    seller_name = serializers.SerializerMethodField(method_name='get_seller')

    class Meta:
        model = Service
        fields = [
            'id', 'seller', 'seller_name', 'title', 'description', 
            'price', 'category', 'delivery_time', 'reviews', 'created_at', 'updated_at'
        ]
    def get_seller(self, obj):
            if obj.seller:
                return obj.buyer.get_full_name() or obj.seller.email
            return None

