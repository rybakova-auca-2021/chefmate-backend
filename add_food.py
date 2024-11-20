import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from preferences.models import Food  # Adjust the import based on your actual app and model name

def add_foods_to_database(foods):
    """
    Add a list of food items to the database.
    Args:
        foods (list of str): List of food names to add.
    """
    food_objects = [Food(name=name) for name in foods]
    Food.objects.bulk_create(food_objects, ignore_conflicts=True) 
    print(f"Added {len(food_objects)} food items to the database.")

if __name__ == "__main__":
    foods_to_add = [
        "Pizza", "Burger", "Pasta", "Sushi", "Tacos",
        "Sandwich", "Salad", "Steak", "Burrito", "Fried Chicken",
        "Spring Rolls", "Ramen", "Paella", "Curry", "Fajitas",
        "Chicken Wings", "Lasagna", "Fish and Chips", "Hot Dog",
        "Dumplings", "Baked Ziti", "Shawarma", "Noodles", "Clams",
        "Tempura", "Goulash", "Kebab", "Falafel", "Moussaka", "Peking Duck"
    ]

    add_foods_to_database(foods_to_add)
    print("Food items have been added successfully!")
