from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('categories_detail', args=[self.id])

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ['name']
    
    def get_absolute_url(self):
        return reverse('ingredients_detail', args=[self.id])


    def __str__(self):
        return self.name
    
# SIMPLE ManyToMany = Django automatically cretes the Junction table for us
# It onle stores both side's IDs. We can add extra fields
# class RecipeIngredient(models.Model):
#     ingresients = models.ManyToManyField(Ingredients)

# ManyToMany with THROUGH - We define the Junction table ouselves
# We can add whatever fields we need (quantity, unit, etc...)
# class Recipe(models.Model):
#     ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")

class RecipeIngredient(models.Model):

    UNIT_CHOICES = [
        ('cup', 'Cup'),
        ('tbsp', 'Tablespoon'),
        ('tsp', 'Teaspoon'),
        ('g', 'Grams'),
        ('kg', 'Kilograms'),
        ('ml', 'Milliliters'),
        ('L', 'Liters'),
        ('oz', 'Ounces'),
        ('lb', 'Pounds'),
        ('piece', 'Piece'),
        ('pinch', 'Pinch'),
        ('to_taste', 'To Taste'),
    ]

    recipe = models.ForeignKey(
        'Recipe', 
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )

    ingredient = models.ForeignKey(
        Ingredient, 
        on_delete=models.PROTECT,
        related_name='ingredient_recipes'
    )

    quantity = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        null=True,
        blank=True
    )

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        blank=True
    )

    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Recipe Ingredient'
        verbose_name_plural = 'Recipe Ingredients'
        unique_together = ['recipe', 'ingredient']

    def __str__(self):
        return f"{self.ingredient.name} -> {self.recipe.title}"
    
# Auxiliar Methods
def recipe_image_path(instance, filename):
    """Saves the image to the media/recipes/<author_id>/<filename>"""
    return f"recipes/{instance.author.id}/{filename}"

class Recipe(models.Model):

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    instructions = models.TextField()
    prep_time = models.PositiveBigIntegerField(help_text="Time in minutes")
    cook_time = models.PositiveBigIntegerField(help_text="Time in minutes")
    servings = models.PositiveIntegerField(default=2)
    image = models.ImageField(
        upload_to=recipe_image_path, 
        blank=True, 
        null=True
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='recipes'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient, 
        through=RecipeIngredient,
        related_name='recipes'
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-created_at']  

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def total_time(self):
        return self.prep_time + self.cook_time
















