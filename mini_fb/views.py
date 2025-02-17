'''
File: views.py
Description: Handles the Facebook web app views, including showing all the profiles at once and showing one at a time
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-02-16
Last Modified: 2025-02-16
'''

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

class ShowAllProfileViews(ListView):
    '''Display all the profiles in our database.'''
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"

    # use of naming convention here, plural form of model
    context_object_name = "profiles"


class ShowProfilePageView(DetailView):
    '''Display a single profile.'''
    model = Profile
    template_name = "mini_fb/show_profile.html"
