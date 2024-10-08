from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.AddIngredientItemView.as_view(), name='add_ingredient_item'),
    path('edit/<int:pk>/', views.EditIngredientItemView.as_view(), name='edit_ingredient_item'),
    path('view/', views.ViewAllIngredientItemsView.as_view(), name='view_all_ingredient_items'),
    path('delete/<int:pk>/', views.DeleteIngredientItemView.as_view(), name='delete_ingredient_item'),
    path('delete_all/', views.DeleteAllIngredientItemsView.as_view(), name='delete_all_ingredient_items'),
]
