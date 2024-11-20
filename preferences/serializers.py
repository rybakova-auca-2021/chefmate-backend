from rest_framework import serializers
from .models import Cuisine, Food

class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ['id', 'name']

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name']

class CreateFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['name']
