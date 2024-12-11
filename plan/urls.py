from django.urls import path
from .views import MealPlanView, BulkMealPlanView

urlpatterns = [
    path('meal-plan/', MealPlanView.as_view(), name='meal-plan'),
    path('bulk-meal-plan/', BulkMealPlanView.as_view(), name='bulk-meal-plan'),
]
