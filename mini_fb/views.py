'''
File: views.py
Description: Handles the Facebook web app views, including showing all the profiles at once, showing one at a time, creating profiles, and creating status messages.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-02-16
Last Modified: 2025-03-02
'''

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse # allows us to create a URL from a URL pattern name

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

class CreateStatusMessageView(CreateView):
    '''A view to handle the creation of new Status Messages for Profiles.'''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect a user after successfully creating a new status message.'''

        # create and return a URL
        # get the primary key from the URL pattern
        pk = self.kwargs['pk']
        return reverse("show_profile", kwargs={'pk': pk})
    
    def get_context_data(self):
        '''Return a dictionary of context variables for use in the template.'''

        # call superclass method
        context = super().get_context_data()

        # get the primary key from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add this profile into context data\
        context["profile"] = profile

        return context

    
    def form_valid(self, form):
        ''' 
        This method handles the form submission and saves the new object to the Django db. 
        We need to add the foreign key of the Profile to the status message before adding it to the db.
        '''

        # get the primary key from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # attach this profile to the status message
        form.instance.profile = profile

        # delegate work to the superclass method form_valid
        return super().form_valid(form)
        