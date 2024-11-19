from django.urls import path

from grocery import views


urlpatterns = [
    path('add/', views.AddGroceryItemView.as_view(), name='add_grocery_item'),
    path('edit/<int:pk>/', views.EditGroceryItemView.as_view(), name='edit_grocery_item'),
    path('view/', views.ViewAllGroceryItemsView.as_view(), name='view_all_grocery_items'),
    path('delete/<int:pk>/', views.DeleteGroceryItemView.as_view(), name='delete_grocery_item'),
    path('delete_all/', views.DeleteAllGroceryItemsView.as_view(), name='delete_all_grocery_items'),
    path('add/groceries/', views.AddMultipleGroceryItemsView.as_view(), name='delete_all_grocery_items'),
]
