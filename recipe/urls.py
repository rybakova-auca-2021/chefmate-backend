# urls.py
from django.urls import path
from .views import FilteredRecipeListView, PopularRecipesView, CuratedCollectionsView, RecipeDetailView, RecipeSearchView, RecipesByCollectionView, ToggleFavoriteView, UserFavoriteRecipesView

urlpatterns = [
    path('recipes/popular/<str:period>/', PopularRecipesView.as_view(), name='popular-recipes'),
    path('collections/', CuratedCollectionsView.as_view(), name='curated-collections'),
    path('collection/<int:collection_id>/recipes/', RecipesByCollectionView.as_view(), name='recipes_by_collection'),
    path('recipes/<int:id>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipes/search/', RecipeSearchView.as_view(), name='recipe-search'),
    path('recipes/filter/', FilteredRecipeListView.as_view(), name='recipe-filter'),
    path('recipes/<int:recipe_id>/favorite/', ToggleFavoriteView.as_view(), name='add_to_favorite'),
    path('favorites/', UserFavoriteRecipesView.as_view(), name='user_favorite_recipes'),
]
