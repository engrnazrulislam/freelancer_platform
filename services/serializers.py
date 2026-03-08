from rest_framework import serializers
from services.models import Service, Category, ServiceReview, ServiceImage
from django.contrib.auth import get_user_model
User = get_user_model()

class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name']

    def get_name(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name if full_name else obj.email
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ServiceImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ServiceImage
        fields = ['id','image']

        def get_image(self, obj):
            return obj.image.url

class ServiceSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)
    seller = SimpleUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    class Meta:
        model = Service
        fields = [
            'id','seller','title','description',
            'images','price','category','category_id',
            'created_at','updated_at','delivery_time','is_active',
        ]
        read_only_fields = ['seller','created_at','updated_at']

class ServiceReviewSerializer(serializers.ModelSerializer):
    buyer_name = serializers.SerializerMethodField()

    class Meta:
        model = ServiceReview
        fields = ['id','buyer','buyer_name','rating','review','created_at']
        read_only_fields = ['buyer', 'created_at']

    def get_buyer_name(self, obj):
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
    seller_name = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'seller', 'seller_name', 'title', 'description', 
            'price', 'category', 'delivery_time', 'images','reviews', 'created_at', 'updated_at'
        ]

    def get_seller_name(self, obj):
        if obj.seller:
            return obj.seller.get_full_name() or obj.seller.email
        return None

