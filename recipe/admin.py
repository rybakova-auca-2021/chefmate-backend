# admin.py
from django.contrib import admin
from .models import Recipe, Collection

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_desc', 'time', 'difficulty', 'number_of_people', 'popularity')
    list_editable = ('popularity',)
    search_fields = ('name', 'short_desc', 'description')
    list_filter = ('difficulty', 'created_at')
    ordering = ('-popularity', 'name')

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    filter_horizontal = ('recipes',)  

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Collection, CollectionAdmin)
