'''
File: views.py
Description: Handles the Facebook web app views, including showing all the profiles at once and showing one at a time
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-02-16
Last Modified: 2025-03-02
'''

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile
from .forms import CreateProfileForm

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

class CreateProfileView(CreateView):
    '''
    A view to handle the creation of a new Profile. 
    (1) After a GET request, display the HTML form to the user
    (2) Process the form submission and store the new Profile
    
    '''

    # choose form class to use, which helps define different fields to display with their data types
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"
