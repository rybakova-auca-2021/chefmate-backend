# models.py
from django.db import models
from django.utils import timezone
from django.conf import settings

from preferences.models import Cuisine

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('dessert', 'Dessert'),
    ]

    POPULARITY_PERIOD_CHOICES = [
        ('today', 'Today'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('none', 'None'),  # Для случаев, если популярность не указана
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    short_desc = models.CharField(max_length=255)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, related_name='cuisine')
    time = models.CharField(max_length=50)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    difficulty = models.CharField(max_length=50)
    number_of_people = models.CharField(max_length=10)
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    ingredients = models.TextField(help_text="Comma-separated list of ingredients")
    steps = models.TextField(help_text="Step-by-step cooking instructions")
    created_at = models.DateTimeField(auto_now_add=True)
    is_vegetarian = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    is_budget_friendly = models.BooleanField(default=False)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='lunch',
        help_text="Category of the recipe",
    )
    popularity = models.CharField(
        max_length=10,
        choices=POPULARITY_PERIOD_CHOICES,
        default='none',
        help_text="Период популярности рецепта"
    )

    def __str__(self):
        return self.name


class Collection(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    recipes = models.ManyToManyField(Recipe, related_name='collections')

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')