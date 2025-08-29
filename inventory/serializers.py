from rest_framework import serializers
from .models import Category, InventoryItem, InventoryChange

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class InventoryItemSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.id')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = InventoryItem
        fields = (
            'id', 'name', 'description', 'quantity', 'price',
            'category', 'category_name', 'date_added', 'last_updated', 'created_by'
        )
        read_only_fields = ('date_added', 'last_updated', 'created_by')

    def validate(self, attrs):
        if 'name' in attrs and not attrs['name'].strip():
            raise serializers.ValidationError({'name': 'Name is required.'})
        if 'price' in attrs and attrs['price'] is None:
            raise serializers.ValidationError({'price': 'Price is required.'})
        if 'quantity' in attrs and attrs['quantity'] is None:
            raise serializers.ValidationError({'quantity': 'Quantity is required.'})
        return attrs

class InventoryChangeSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.name')
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = InventoryChange
        fields = ('id', 'item', 'item_name', 'user', 'user_email', 'old_quantity', 'new_quantity', 'timestamp')
        read_only_fields = ('user', 'old_quantity', 'new_quantity', 'timestamp')
