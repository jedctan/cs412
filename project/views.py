'''
File: views.py
Description: Define views for the digital wardrobe app.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-04-13
'''
from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import ClothingItem
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *

from django.shortcuts import render, redirect
from .models import ClothingItem, Outfit

def create_outfit(request):
    '''Function-based view to create a custom form with image selection.'''

    # NOTE: I used a function-based view here instead of ModelForm so I could have more control
    # over the form so I could use radio buttons with images for clothing selection. This approach
    # also ended up being much more simpler than previous attempts to override widgets in a ModelForm.

    # if the user clicked the create outfit button (POST)
    if request.method == 'POST':

        # get the form data
        name = request.POST.get('name')
        notes = request.POST.get('notes')
        hat_id = request.POST.get('hat')
        jacket_id = request.POST.get('jacket')
        shirt_id = request.POST.get('shirt')
        bottoms_id = request.POST.get('bottoms')
        shoes_id = request.POST.get('shoes')
        
        # get the clothing items based on the IDs
        hat = ClothingItem.objects.filter(id=hat_id).first() if hat_id else None
        jacket = ClothingItem.objects.filter(id=jacket_id).first() if jacket_id else None
        shirt = ClothingItem.objects.filter(id=shirt_id).first() if shirt_id else None
        bottoms = ClothingItem.objects.filter(id=bottoms_id).first() if bottoms_id else None
        shoes = ClothingItem.objects.filter(id=shoes_id).first() if shoes_id else None

        # create the outfit with the selected clothing items
        Outfit.objects.create(
            user=request.user,
            name=name,
            notes=notes,
            hat=hat,
            jacket=jacket,
            shirt=shirt,
            bottoms=bottoms,
            shoes=shoes
        )
        # redirect to the outfit list page after creating the outfit
        return redirect('outfit_list') 

    # if they didn't submit, then show the form (GET)

    # get all clothing items for the user
    hats = ClothingItem.objects.filter(category='hat', user=request.user)
    jackets = ClothingItem.objects.filter(category='jacket', user=request.user)
    shirts = ClothingItem.objects.filter(category='shirt', user=request.user)
    bottoms = ClothingItem.objects.filter(category='bottom', user=request.user)
    shoes = ClothingItem.objects.filter(category='shoes', user=request.user)

    # loads template, adds all of the clothing items, returns the response
    return render(request, 'project/create_outfit_custom.html', {
        'hats': hats,
        'jackets': jackets,
        'shirts': shirts,
        'bottoms': bottoms,
        'shoes': shoes
    })

from django.shortcuts import get_object_or_404

def edit_outfit_custom(request, pk):
    '''Function-based view to edit an existing outfit using visual selection.'''

    # get the outfit by primary key (pk) and user
    outfit = Outfit.objects.get(pk=pk, user=request.user)
    
    # NOTE: FBV was used here for similar reasons as create_outfit. See above.

    # if the user submitted the form (POST)
    if request.method == 'POST':

        # update the outfit with the form data
        outfit.name = request.POST.get('name')
        outfit.notes = request.POST.get('notes')
        outfit.season = request.POST.get('season')
        outfit.occasion = request.POST.get('occasion')

        # get the clothing item IDs from the form
        hat_id = request.POST.get('hat')
        jacket_id = request.POST.get('jacket')
        shirt_id = request.POST.get('shirt')
        bottoms_id = request.POST.get('bottoms')
        shoes_id = request.POST.get('shoes')

        # update the outfit's clothing items based on the selected IDs
        outfit.hat = ClothingItem.objects.filter(id=hat_id).first() if hat_id else None
        outfit.jacket = ClothingItem.objects.filter(id=jacket_id).first() if jacket_id else None
        outfit.shirt = ClothingItem.objects.filter(id=shirt_id).first() if shirt_id else None
        outfit.bottoms = ClothingItem.objects.filter(id=bottoms_id).first() if bottoms_id else None
        outfit.shoes = ClothingItem.objects.filter(id=shoes_id).first() if shoes_id else None
        
        # save to db
        outfit.save()

        # redirect to the outfit detail page after updating
        return redirect('outfit_detail', pk=outfit.pk)

    # if they didn't submit, then show the form (GET)

    # get all clothing items for the user
    hats = ClothingItem.objects.filter(category='hat', user=request.user)
    jackets = ClothingItem.objects.filter(category='jacket', user=request.user)
    shirts = ClothingItem.objects.filter(category='shirt', user=request.user)
    bottoms = ClothingItem.objects.filter(category='bottom', user=request.user)
    shoes = ClothingItem.objects.filter(category='shoes', user=request.user)


    # loads template, adds the outfit and all of the clothing items, returns the response
    return render(request, 'project/update_outfit_custom.html', {
        'outfit': outfit,
        'hats': hats,
        'jackets': jackets,
        'shirts': shirts,
        'bottoms': bottoms,
        'shoes': shoes,
    })

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

    context_object_name = "clothing_items"

    def get_queryset(self):
        '''Return clothing based on the current user and any filters applied.'''

        # ensure items for this user
        clothing = ClothingItem.objects.filter(user=self.request.user)

        # category
        if 'category' in self.request.GET:
            category = self.request.GET['category']
            if category:
                clothing = clothing.filter(category=category)
        
        # brand
        if 'brand' in self.request.GET:
            brand = self.request.GET['brand']
            if brand:
                clothing = clothing.filter(brand=brand)

        # color
        if 'color' in self.request.GET:
            color = self.request.GET['color']
            if color:
                clothing = clothing.filter(color=color)
        
        # season
        if 'season' in self.request.GET:
            season = self.request.GET['season']
            if season:
                clothing = clothing.filter(season=season)

        return clothing
    
    def get_context_data(self, **kwargs):
        '''Add query params to the template.'''

        context = super().get_context_data(**kwargs)
        context['categories'] = ClothingItem.CATEGORY_CHOICES   
        context['brands'] = ClothingItem.objects.filter(user=self.request.user).values_list('brand', flat=True).distinct()
        context['colors'] = ClothingItem.objects.filter(user=self.request.user).values_list('color', flat=True).distinct()
        context['seasons'] = ClothingItem.SEASON_CHOICES
        return context

class CreateClothingItemView(CustomLoginRequiredMixin, CreateView):
    '''
    View to handle creation of clothing items.
    1. After GET request, display form to the user.
    2. Then process form submission, and store in the db.
    '''

    form_class = CreateClothingItemForm
    template_name = "project/create_clothing_item_form.html"

    def form_valid(self, form):
        '''Process the form submission and save the clothing item.'''
        # set user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        '''Provide a URL to redirect a user after successfully adding a clothing item.'''
        return reverse("show_wardrobe")

class ShowOutfitsView(CustomLoginRequiredMixin, ListView):
    '''Display all the clothing items.'''
    model = Outfit
    template_name = "project/show_outfits.html"

    context_object_name = "outfits"

    def get_queryset(self):
        '''Return outfits based on the current user and any filters applied.'''

        # ensure outfits for this user
        queryset = Outfit.objects.filter(user=self.request.user)

        # filter by name, season, and occasion
        name_query = self.request.GET.get("name")
        if name_query:
            queryset = queryset.filter(name__icontains=name_query)

        season = self.request.GET.get("season")
        if season:
            queryset = queryset.filter(season=season)

        occasion = self.request.GET.get("occasion")
        if occasion:
            queryset = queryset.filter(occasion=occasion)

        return queryset
    
    def get_context_data(self, **kwargs):
        '''Add query params to the template.'''
        context = super().get_context_data(**kwargs)
        context["seasons"] = Outfit.SEASON_CHOICES
        context["occasions"] = Outfit.OCCASION_CHOICES
        context["request"] = self.request
        return context
    

class ShowClothingItemDetail(DetailView):
    '''Display the details of a clothing item.'''
    model = ClothingItem
    template_name = "project/clothing_item_detail.html"
    context_object_name = "item"

    def get_queryset(self):
        '''Return only the clothing items belonging to the current user.'''
        return ClothingItem.objects.filter(user=self.request.user)

class ShowOutfitDetail(DetailView):
    '''Display the details of an outfit.'''
    model = Outfit
    template_name = "project/outfit_detail.html"
    context_object_name = "outfit"
    
    def get_queryset(self):
        '''Return only the outfits belonging to the current user.'''
        return Outfit.objects.filter(user=self.request.user)

class UpdateClothingItemView(CustomLoginRequiredMixin, UpdateView):
    '''View to update a clothing item.'''
    model = ClothingItem
    form_class = UpdateClothingItemForm
    template_name = "project/update_clothing_item_form.html"

    def get_queryset(self):
        '''Ensure only items belonging to the user can be updated.'''
        return ClothingItem.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        '''Add a cancel URL to the context for the update form.'''
        context = super().get_context_data(**kwargs)
        # create cancel URL with pk
        context['cancel_url'] = reverse('item_detail', kwargs={'pk': self.object.pk})
        return context

    def get_success_url(self):
        '''Return the URL to redirect to after successfully updating an item.'''
        return reverse('show_wardrobe')

class DeleteClothingItemView(CustomLoginRequiredMixin, DeleteView):
    '''View to delete a clothing item.'''
    model = ClothingItem
    template_name = "project/delete_confirm.html"

    def get_success_url(self):
        '''Return the URL to redirect to after successfully deleting an item.'''
        return reverse("show_wardrobe")
    
    def get_queryset(self):
        '''Ensure only items belonging to the user can be deleted.'''
        return ClothingItem.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        '''Add a cancel URL to the context for the delete form.'''
        context = super().get_context_data(**kwargs)
        # create cancel URL with pk
        context['cancel_url'] = reverse('item_detail', kwargs={'pk': self.object.pk})
        return context


class DeleteOutfitView(CustomLoginRequiredMixin, DeleteView):
    '''View to delete an outfit.'''
    model = Outfit
    template_name = "project/delete_confirm.html"

    # redirect to the wardrobe after deleting an outfit
    def get_success_url(self):
        return reverse("show_wardrobe")
    
    # user can only delete their own outfits
    def get_queryset(self):
        return Outfit.objects.filter(user=self.request.user)
      
    def get_context_data(self, **kwargs):
        '''Add a cancel URL to the context for the delete form.'''
        context = super().get_context_data(**kwargs)
        # create cancel URL with pk
        context['cancel_url'] = reverse('outfit_detail', kwargs={'pk': self.object.pk})
        return context