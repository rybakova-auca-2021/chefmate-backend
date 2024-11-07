# serializers.py
from rest_framework import serializers
from .models import Favorite, Recipe, Collection

class PopularRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'number_of_people', 'time', 'image_url']

class RecipeSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'description', 'short_desc', 'time', 'difficulty',
            'number_of_people', 'protein', 'carbs', 'fat', 'ingredients', 'steps', 'image_url', 'is_favorite'
        ]

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=obj).exists()
        return False

class CollectionSerializer(serializers.ModelSerializer):
    recipes = PopularRecipeSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'recipes', 'image_url']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'recipe', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']