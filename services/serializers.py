from rest_framework import serializers
from services.models import Service, Category
class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField(method_name='get_category_name')
    class Meta:
        model = Service
        fields = ['id','seller','title','description','price','category','created_at','updated_at','delivery_time']
        read_only_fields = ['seller','created_at','updated_at']
    def get_category_name(self):
        return Category.objects.prefetch_related('category_services').filter(name=self.category_name)