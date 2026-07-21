from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from .models import Recipe, RecipeIngredient

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit', 'notes']
        widgets = {
            'ingredient': forms.Select(attrs={
                'class': 'form-select form-selct-sm',
                }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '0.0',
                'step': '0.01',
                }),
            'unit': forms.Select(attrs={
                'class': 'form-select form-select-sm',
                }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'e.g. finely chopped',
                }),
        }

RecipeIngredientFormSet = inlineformset_factory(
    parent_model=Recipe,
    model=RecipeIngredient,
    form=RecipeIngredientForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True,    
)

#____________________ Recipe Form ______________________
class RecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False # we control the <form> tag in the template
        self.helper.layout = Layout(
            Field('title'),
            Row(
                Column('category', css_class='col-md-6'),
                Column('status', css_class='col-md-6'),
            ),
            Field('description'),
            Field('instructions'),
            Row(
                Column('prep_time', css_class='col-md-4'),
                Column('cook_time', css_class='col-md-4'),
                Column('servings', css_class='col-md-4'),
            ),
            Field('image'),
        )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'instructions', 'prep_time', 'cook_time', 'servings', 'image', 'category', 'status']
        # slug and author are excluded intentioinally
        # slug -> auto generated in model's save()
        # author -> assigned in view from request.user
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'instructions': forms.Textarea(attrs={'rows': 8}),
            'prep_time': forms.NumberInput(attrs={'placeholder': 'Minutes'}),
            'cook_time': forms.NumberInput(attrs={'placeholder': 'Minutes'}),
        }
        labels = {
            'prep_time': 'Prep Time (min)',
            'cook_time': 'Cook Time (min)',
        }

    # We start from specifics clean_fieldname
    def clean_title(self):
        title = self.cleaned_data.get('title')
        qs = Recipe.objects.filter(author=self.user, title__iexact=title)
        # On update, exclude the current instance from the check
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "You already have a recipe with this title."
            )
        
        return title # Always return the cleaned title
    
    # To generate extra validations
    def clean(self):
        cleaned_data = super().clean()
        prep_time = cleaned_data.get('prep_time')
        cook_time = cleaned_data.get('cook_time')
        
        if prep_time is not None and cook_time is not None:
            if prep_time + cook_time > 1440: # 24 hours in minutes
                raise forms.ValidationError("Total cooking time (prep + cook) cannot exceed 24 hours.")
            
            if prep_time == 0 and cook_time == 0:
                raise forms.ValidationError("At least one of the prep time or cook time must be greater than 0.")
            
        return cleaned_data

    
        


            
        
        