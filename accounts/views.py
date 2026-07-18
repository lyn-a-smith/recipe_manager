from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class SignUpView(CreateView):
    template_name = "registration/signup.html"
    # form_class attribute allows us to create objects froma python class
    # we use this whenwe want to have a custom form
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
