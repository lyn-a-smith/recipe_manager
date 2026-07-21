from django.shortcuts import render
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
    )
from .models import Category, Ingredient
from django.urls import reverse_lazy

# Create your views here.
# Ingredients
class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredients/list.html'
    context_object_name = 'ingredients'
    # paginate_by = 10

class IngredientDetailView(DetailView):
    model = Ingredient
    template_name = 'ingredients/detail.html'
    context_object_name = 'ingredient'

class IngredientCreateView(CreateView):
    model = Ingredient
    template_name = 'ingredients/new.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('ingredients_list')

class IngredientUpdateView(UpdateView):
    template_name = 'ingredients/edit.html'
    model = Ingredient
    fields = ['name', 'description']
    

class IngredientDeleteView(DeleteView):
    template_name = 'ingredients/delete.html'
    model = Ingredient
    success_url = reverse_lazy('ingredients_list')

# Categories
class CategoryListView(ListView):
    model = Category
    template_name = 'categories/list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/detail.html'
    context_object_name = 'category'

class CategoryCreateView(CreateView):
    model = Category
    template_name = 'categories/new.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('categories_list')

class CategoryUpdateView(UpdateView):
    template_name = 'categories/edit.html'
    model = Category
    fields = ['name', 'description']

class CategoryDeleteView(DeleteView):
    template_name = 'categories/delete.html'
    model = Category
    success_url = reverse_lazy('categories_list')






