from rest_framework import serializers
from .models import GroceryItem

class GroceryItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  

    class Meta:
        model = GroceryItem
        fields = ['id', 'user', 'name', 'quantity']
