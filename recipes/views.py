from django.shortcuts import render
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
    )
from .models import Category, Ingredient, Recipe
from .forms import RecipeForm, RecipeIngredientFormSet
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

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

#_________________ Recipe CRUD ______________________
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/list.html'
    context_object_name = 'recipes'
    paginate_by = 9

    def get_queryset(self):
        # Only show published recipes to the public
        return Recipe.objects.filter(status='published').select_related('author', 'category')

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = RecipeIngredientFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context['ingredient_formset'] = RecipeIngredientFormSet(
                instance=self.object
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        ingredient_formset = context['ingredient_formset']

        if ingredient_formset.is_valid():
            form.instance.author = self.request.user
            self.object = form.save()

            #link formset to the newly created recipe, then save
            ingredient_formset.instance = self.object
            ingredient_formset.save()

            messages.success(self.request, " Recipe created successfully!")
            return super().form_valid(form)

        return self.render_to_response(context)

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    context_object_name = 'recipe'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Recipe.objects.select_related('author', 'category').prefetch_related('recipe_ingredients__ingredient')











