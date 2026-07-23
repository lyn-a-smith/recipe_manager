from django.urls import path
from .views import (
    IngredientCreateView,
    IngredientListView,
    IngredientDetailView,
    IngredientUpdateView,
    IngredientDeleteView,
    CategoryCreateView,
    CategoryListView,
    CategoryDetailView,
    CategoryUpdateView,
    CategoryDeleteView,
    RecipeListView,
    RecipeCreateView,
    RecipeDetailView,
)

urlpatterns = [
    path('ingredients/', IngredientListView.as_view(), name='ingredients_list'),
    path('ingredients/new/', IngredientCreateView.as_view(), name='ingredients_new'),
    path('ingredients/detail/<int:pk>/', IngredientDetailView.as_view(), name='ingredients_detail'),
    path('ingredients/edit/<int:pk>/', IngredientUpdateView.as_view(), name='ingredients_edit'),
    path('ingredients/delete/<int:pk>/', IngredientDeleteView.as_view(), name='ingredients_delete'),
    path('categories/', CategoryListView.as_view(), name='categories_list'),
    path('categories/new/', CategoryCreateView.as_view(), name='categories_new'),
    path('categories/detail/<int:pk>/', CategoryDetailView.as_view(), name='categories_detail'),
    path('categories/edit/<int:pk>/', CategoryUpdateView.as_view(), name='categories_edit'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='categories_delete'),
    #________________ URLs for Recipe _____________________
    path('', RecipeListView.as_view(), name='recipes_list'),
    path('new/', RecipeCreateView.as_view(), name='recipes_create'),
    path('<slug:slug>/', RecipeDetailView.as_view(), name='recipes_detail'),
    
    
]