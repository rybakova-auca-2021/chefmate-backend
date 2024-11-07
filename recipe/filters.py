# filters.py
from django_filters import rest_framework as filters
from .models import Recipe
import re

def number_of_people_filter(queryset, name, value):
    """Custom filter method to handle number of people range."""
    if value:
        if '-' in value:
            try:
                start, end = map(int, value.split('-'))
                return queryset.filter(number_of_people__gte=start, number_of_people__lte=end)
            except ValueError:
                raise ValueError("Range should be in the format 'start-end', e.g., '6-10'")
        else:
            try:
                exact_value = int(value)
                return queryset.filter(number_of_people=exact_value)
            except ValueError:
                raise ValueError("Exact value should be an integer.")
    return queryset



def parse_time_to_minutes(time_str):
    """Convert a time string to minutes."""
    match = re.match(r'(\d+)', time_str)
    if match:
        return int(match.group(1))
    return None

def time_filter(queryset, name, value):
    """Custom filter method to handle time range."""
    if value:
        if '-' in value:
            start_time_str, end_time_str = value.split('-')
            start_minutes = parse_time_to_minutes(start_time_str)
            end_minutes = parse_time_to_minutes(end_time_str)
            if start_minutes is not None and end_minutes is not None:
                return queryset.filter(time__range=(f'~{start_minutes}', f'~{end_minutes}'))
        else:
            return queryset.filter(time=value)
    return queryset

class RecipeFilter(filters.FilterSet):
    time = filters.CharFilter(method=time_filter) 
    number_of_people = filters.CharFilter(method=number_of_people_filter)  
    difficulty = filters.ChoiceFilter(
        choices=[
            ('super easy', 'super easy'),
            ('not too tricky', 'not too tricky'),
            ('showing off', 'showing off')
        ]
    )
    is_vegetarian = filters.BooleanFilter(field_name="is_vegetarian", label="vegetarian")
    is_gluten_free = filters.BooleanFilter(field_name="is_gluten_free", label="gluten-free")
    is_budget_friendly = filters.BooleanFilter(field_name="is_budget_friendly", label="budget-friendly")

    class Meta:
        model = Recipe
        fields = ['time', 'number_of_people', 'difficulty', 'is_vegetarian', 'is_gluten_free', 'is_budget_friendly']
