# food_app/urls.py

from django.urls import path
from .views import AddPreferredCuisinesView, AddPreferredFoodView, FetchCuisinesView, FetchFoodView, RetrievePreferredCuisinesView, RetrievePreferredFoodView

urlpatterns = [
    path('fetch-cuisines/', FetchCuisinesView.as_view(), name='fetch_cuisines'),
    path('fetch-food/', FetchFoodView.as_view(), name='fetch_food'),
    path('cuisines/add-preferred/', AddPreferredCuisinesView.as_view(), name='add-preferred-cuisines'),
    path('food/add-preferred/', AddPreferredFoodView.as_view(), name='add-preferred-food'),
     path('cuisines/preferred/', RetrievePreferredCuisinesView.as_view(), name='retrieve-preferred-cuisines'),
    path('food/preferred/', RetrievePreferredFoodView.as_view(), name='retrieve-preferred-food'),
]
