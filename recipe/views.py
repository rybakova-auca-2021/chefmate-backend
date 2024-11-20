# views.py
from datetime import timedelta
import random
from django.utils import timezone
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Favorite
from django.core.cache import cache
from django.db.models import Q

from recipe.filters import RecipeFilter
from .models import Recipe, Collection
from .serializers import FavoriteSerializer, PopularRecipeSerializer, RecipeSerializer, CollectionSerializer
from django_filters.rest_framework import DjangoFilterBackend


class PopularRecipesView(APIView):
    def get(self, request, period):
        time_filter = timezone.now()
        
        # Adjust time filter based on period
        if period == 'today':
            time_filter -= timedelta(days=1)
        elif period == 'week':
            time_filter -= timedelta(weeks=1)
        elif period == 'month':
            time_filter -= timedelta(days=30)
        else:
            return Response({"error": "Invalid period specified"}, status=400)
        
        recipes = Recipe.objects.filter(created_at__gte=time_filter).order_by('-popularity')
        
        serializer = PopularRecipeSerializer(recipes, many=True)
        
        return Response(serializer.data)

class CuratedCollectionsView(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class RecipeDetailView(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = 'id'

    def get_serializer_context(self):
        return {'request': self.request}

class RecipeSearchView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = PopularRecipeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description'] 

class FilteredRecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

class RecipesByCollectionView(generics.ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        collection_id = self.kwargs['collection_id'] 
        return Recipe.objects.filter(collections__id=collection_id) 

class ToggleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request, recipe_id):
        user = request.user
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorite.objects.get_or_create(user=user, recipe=recipe)
        
        if created:
            serializer = FavoriteSerializer(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            favorite.delete()
            return Response({"message": "Recipe removed from favorites"}, status=status.HTTP_200_OK)
    
class UserFavoriteRecipesView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.filter(favorited_by__user=user)

    def get_serializer_context(self):
        return {'request': self.request}
    

class RecipeOfTheDayView(APIView):
    """
    Returns one random recipe as the recipe of the day based on the user's preferences.
    The recipe is selected once per day and cached.
    """

    CACHE_KEY = "recipe_of_the_day"
    CACHE_TIMEOUT = 60 * 60 * 24  # Cache for 24 hours

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        # Try to fetch the recipe from the cache
        cached_recipe_id = cache.get(self.CACHE_KEY)

        if cached_recipe_id:
            try:
                recipe_of_the_day = Recipe.objects.get(id=cached_recipe_id)
            except Recipe.DoesNotExist:
                cache.delete(self.CACHE_KEY)  # Clear invalid cache
                return Response({"error": "No recipe available"}, status=404)
        else:
            # Filter recipes based on user preferences
            preferred_cuisines = user.preferred_cuisines.values_list('name', flat=True)
            preferred_food = user.preferred_food.values_list('name', flat=True)

            recipes = Recipe.objects.filter(
                Q(cuisine__name__in=preferred_cuisines) | 
                Q(ingredients__icontains=preferred_food)
            ).distinct()

            if not recipes.exists():
                return Response({"error": "No recipes available for your preferences"}, status=404)

            # Select a random recipe from the filtered list
            random_index = random.randint(0, recipes.count() - 1)
            recipe_of_the_day = recipes[random_index]

            # Cache the selected recipe
            cache.set(self.CACHE_KEY, recipe_of_the_day.id, self.CACHE_TIMEOUT)

        # Assuming PopularRecipeSerializer exists and is implemented correctly
        serializer = PopularRecipeSerializer(recipe_of_the_day, context={'request': request})
        return Response(serializer.data, status=200)
