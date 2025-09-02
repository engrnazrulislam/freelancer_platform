from rest_framework import serializers
from services.models import Service, Category, ServiceReview

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    class Meta:
        model = Service
        fields = ['id','seller','title','description','price','category','category_id','created_at','updated_at','delivery_time']
        read_only_fields = ['seller','created_at','updated_at']

class ServiceReviewSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.get_full_name', read_only=True)
    class Meta:
        model = ServiceReview
        fields = ['id','buyer','buyer_name','rating','review','created_at']
        read_only_fields = ['buyer', 'created_at']

class ServiceDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    reviews = ServiceReviewSerializer(many=True, read_only=True)
    seller_name = serializers.CharField(source='seller.get_full_name', read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'seller', 'seller_name', 'title', 'description', 
            'price', 'category', 'delivery_time', 'reviews', 'created_at', 'updated_at'
        ]
