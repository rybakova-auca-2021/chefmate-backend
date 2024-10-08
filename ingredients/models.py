from django.conf import settings
from django.db import models

class IngredientItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ingredient_items"
    )
    name = models.CharField(max_length=100)
    date_of_manufacture = models.DateField(blank=True, null=True)
    date_of_expiration = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.quantity or 'N/A'}"
