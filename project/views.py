from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, CreateView
from .models import ClothingItem
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *


class CustomLoginRequiredMixin(LoginRequiredMixin):
    '''Custom class to add changes to the LoginRequiredMixin class.'''

    def get_login_url(self):
        '''Return the URL for this app's login page.'''
        # sends us to login screen if we try to create a profile when not logged in
        return reverse('login')

class ShowWardrobeView(CustomLoginRequiredMixin, ListView):
    '''Display all the clothing items.'''
    model = ClothingItem
    template_name = "project/show_wardrobe.html"

    # use of naming convention here, plural form of model
    context_object_name = "clothing_items"

    def get_queryset(self):
        '''Return only the clothing items belonging to the current user.'''
        return ClothingItem.objects.filter(user=self.request.user)

class CreateClothingItemView(CustomLoginRequiredMixin, CreateView):
    '''
    View to handle creation of clothing items.
    1. After GET request, display form to the user.
    2. Then process form submission, and store in the db.
    '''

    form_class = CreateClothingItem
    template_name = "project/create_clothing_item_form.html"

    def form_valid(self, form):
        # set user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        '''Provide a URL to redirect a user after successfully adding a clothing item.'''

        return reverse("show_wardrobe")
    
class CreateOutfitView(CustomLoginRequiredMixin, CreateView):
    '''
    View to handle creation of outfits.
    '''

    form_class = CreateOutfit
    template_name = "project/create_outfit_form.html"

    def form_valid(self, form):
        # set user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        '''Provide a URL to redirect a user after successfully adding a clothing item.'''

        return reverse("show_wardrobe")


