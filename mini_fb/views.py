from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile
# Create your views here.


class ShowAllProfileViews(ListView):
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"

    # use of naming convention here, plural form of model
    context_object_name = "profiles"

