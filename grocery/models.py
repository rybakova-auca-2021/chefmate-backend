from django.conf import settings
from django.db import models

class GroceryItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="grocery_items")
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.quantity or 'N/A'}"
