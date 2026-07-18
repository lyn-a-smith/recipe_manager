from django.contrib import admin
from .models import Category, Ingredient, Recipe, RecipeIngredient


# Register your models here.
admin.site.register([Category, Ingredient, Recipe, RecipeIngredient])
