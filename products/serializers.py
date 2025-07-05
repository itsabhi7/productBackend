from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    stock_status = serializers.CharField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'sku', 'name', 'description', 'category', 'price', 
            'quantity', 'created_at', 'updated_at', 'created_by', 
            'created_by_username', 'stock_status', 'is_in_stock'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class ProductListSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    stock_status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'sku', 'name', 'category', 'price', 'quantity', 
            'created_at', 'created_by_username', 'stock_status'
        ]