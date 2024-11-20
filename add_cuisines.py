import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from preferences.models import Cuisine

def add_cuisines_to_database(cuisines):
    """
    Add a list of cuisines to the database.
    Args:
        cuisines (list of str): List of cuisine names to add.
    """
    cuisine_objects = [Cuisine(name=name) for name in cuisines]
    Cuisine.objects.bulk_create(cuisine_objects, ignore_conflicts=True) 
    print(f"Added {len(cuisine_objects)} cuisines to the database.")

if __name__ == "__main__":
    cuisines_to_add = [
        "Italian", "Mexican", "Indian", "Chinese", "Japanese",
        "French", "Mediterranean", "Thai", "Korean", "Vietnamese",
        "Spanish", "Turkish", "Greek", "Lebanese", "Moroccan",
        "Ethiopian", "Brazilian", "Argentinian", "Peruvian", "Caribbean",
        "German", "Russian", "Polish", "British", "American",
        "Australian", "Filipino", "Pakistani", "Persian", "Cajun"
    ]

    add_cuisines_to_database(cuisines_to_add)
    print("Cuisines have been added successfully!")
