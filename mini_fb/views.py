'''
File: views.py
Description: Handles the Facebook web app views, including showing all the profiles at once, showing one at a time, creating profiles, creating status messages and adding/displaying friends.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-02-16
Last Modified: 2025-03-18
'''

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, Image, StatusImage, StatusMessage, Friend
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusForm
from django.urls import reverse # allows us to create a URL from a URL pattern name
from django.contrib.auth.mixins import LoginRequiredMixin # for authentication    

class CustomLoginRequiredMixin(LoginRequiredMixin):
    '''Custom class to add changes to the LoginRequiredMixin class.'''

    def get_login_url(self):
        '''Return the URL for this app's login page.'''
        # sends us to login screen if we try to create a profile when not logged in
        return reverse('login')


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

class CreateProfileView(CustomLoginRequiredMixin, CreateView):
    '''
    A view to handle the creation of a new Profile. 
    (1) After a GET request, display the HTML form to the user
    (2) Process the form submission and store the new Profile

    '''

    # choose form class to use, which helps define different fields to display with their data types
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"


class CreateStatusMessageView(CustomLoginRequiredMixin, CreateView):
    '''A view to handle the creation of new Status Messages for Profiles.'''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_object(self):
        '''Returns Profile corresponding to the signed in user.'''
        profiles = Profile.objects.filter(user=self.request.user)
        # since admin is associated with multiple profiles, we will return the first no matter what
        return profiles[0]

    def get_success_url(self):
        '''Provide a URL to redirect a user after successfully creating a new status message.'''

        # create and return a URL
        # get the primary key from the URL pattern
        pk = self.get_object().pk
        return reverse("show_profile", kwargs={'pk': pk})
    
    def get_context_data(self):
        '''Return a dictionary of context variables for use in the template.'''

        # call superclass method
        context = super().get_context_data()

        # get the profile
        profile = self.get_object()

        # add this profile into context data
        context["profile"] = profile

        return context

    
    def form_valid(self, form):
        ''' 
        This method handles the form submission and saves the new object to the Django db. 
        We need to add the foreign key of the Profile to the status message before adding it to the db.
        '''

        # PRIMARY KEY HANDLING

        # get the Profile
        profile = self.get_object()

        # attach this profile to the status message
        form.instance.profile = profile

        # STATUSIMAGE HANDLING

        # save the status message to database
        sm = form.save() # StatusMessage object

        # read the file from the form:
        files = self.request.FILES.getlist('files')

        # loop thru inputted files
        for file in files:

            # create Image object and save to DB
            img = Image(profile=profile, image_file=file)
            img.save()

            # create StatusImage object and save to DB
            status_img = StatusImage(image=img, status_message=sm)
            status_img.save() 

        # delegate work to the superclass method form_valid
        return super().form_valid(form)
    
class UpdateProfileView(CustomLoginRequiredMixin, UpdateView):
    '''View class to handle update of a Profile based on its PK.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self):
        '''Returns specific Profile to work with in the template.'''
        profiles = Profile.objects.filter(user=self.request.user)
        # since admin is associated with multiple profiles, we will return the first no matter what
        return profiles[0]
        
class DeleteStatusMessageView(CustomLoginRequiredMixin, DeleteView):
    '''View class to delete a status message on a Profile.'''

    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'

    def get_success_url(self):
        '''Return the URL to redirect to after a successful deletion.'''

        # find PK of the status messaage
        pk = self.kwargs['pk']

        # find status message
        status_message = StatusMessage.objects.get(pk=pk)

        # find the PK for the profile that the status message is associated with
        profile = status_message.profile

        return reverse('show_profile', kwargs={'pk':profile.pk})

class UpdateStatusMessageView(CustomLoginRequiredMixin, UpdateView):
    '''View class to handle update of a status message of a Profile.'''

    model = StatusMessage
    form_class = UpdateStatusForm
    template_name = 'mini_fb/update_status_form.html'

    
class CreateFriendView(CustomLoginRequiredMixin, View):
    '''View class to handle the creation of Friend relations.'''

    def get_object(self):
        '''Returns Profile corresponding to the signed in user.'''
        profiles = Profile.objects.filter(user=self.request.user)
        # since admin is associated with multiple profiles, we will return the first no matter what
        return profiles[0]

    def dispatch(self, request, *args, **kwargs):
        
        # from the request get the 2 primary keys
        pk1 = self.get_object().pk
        pk2 = self.kwargs['other_pk']

        profile1 = Profile.objects.get(pk=pk1)
        profile2 = Profile.objects.get(pk=pk2)

        profile1.add_friend(profile2)
        
        return redirect(reverse('show_profile', kwargs={'pk': profile1.pk}))

class ShowFriendSuggestionsView(DetailView):
    '''View class to display all friend suggestions for a single profile.'''

    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'

    def get_object(self):
        '''Returns Profile corresponding to the signed in user.'''
        profiles = Profile.objects.filter(user=self.request.user)
        # since admin is associated with multiple profiles, we will return the first no matter what
        return profiles[0]
        

class ShowNewsFeedView(DetailView):
    '''View class to display a news feed containing all StatusMessages for a profile and its friends.'''

    model = Profile
    template_name = 'mini_fb/news_feed.html'

    def get_object(self):
        '''Returns Profile corresponding to the signed in user.'''
        profiles = Profile.objects.filter(user=self.request.user)
        # since admin is associated with multiple profiles, we will return the first no matter what
        return profiles[0]