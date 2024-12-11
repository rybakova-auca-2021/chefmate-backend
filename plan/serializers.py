from rest_framework import serializers

from recipe.serializers import RecipeSerializer
from .models import MealPlan


from rest_framework import serializers

class MealPlanSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer()

    class Meta:
        model = MealPlan
        fields = ['id', 'date', 'meal_type', 'recipe']

class MealPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = ['date', 'meal_type', 'recipe']
