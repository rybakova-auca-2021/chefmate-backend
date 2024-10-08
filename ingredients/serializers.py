from rest_framework import serializers
from .models import IngredientItem

class IngredientItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True) 

    class Meta:
        model = IngredientItem
        fields = ['id', 'user', 'name', 'quantity', 'date_of_manufacture', 'date_of_expiration', 'category']
