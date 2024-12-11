from django.db import models

from recipe.models import Recipe

# Create your models here.


class MealPlan(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]
    
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="meal_plans")

    def __str__(self):
        return f"{self.date} - {self.meal_type} - {self.recipe.title}"