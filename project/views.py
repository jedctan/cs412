from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, CreateView
from .models import ClothingItem
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *

from django.shortcuts import render, redirect
from .models import ClothingItem, Outfit

def create_outfit(request):
    '''Function-based view to create a custom form with image selection.'''

    if request.method == 'POST':
        name = request.POST.get('name')
        notes = request.POST.get('notes')

        hat_id = request.POST.get('hat')
        jacket_id = request.POST.get('jacket')
        shirt_id = request.POST.get('shirt')
        bottoms_id = request.POST.get('bottoms')
        shoes_id = request.POST.get('shoes')

        hat = ClothingItem.objects.filter(id=hat_id).first() if hat_id else None
        jacket = ClothingItem.objects.filter(id=jacket_id).first() if jacket_id else None
        shirt = ClothingItem.objects.filter(id=shirt_id).first() if shirt_id else None
        bottoms = ClothingItem.objects.filter(id=bottoms_id).first() if bottoms_id else None
        shoes = ClothingItem.objects.filter(id=shoes_id).first() if shoes_id else None

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

        return redirect('show_wardrobe') 

    hats = ClothingItem.objects.filter(category='hat', user=request.user)
    jackets = ClothingItem.objects.filter(category='jacket', user=request.user)
    shirts = ClothingItem.objects.filter(category='shirt', user=request.user)
    bottoms = ClothingItem.objects.filter(category='bottom', user=request.user)
    shoes = ClothingItem.objects.filter(category='shoes', user=request.user)

    return render(request, 'project/create_outfit_custom.html', {
        'hats': hats,
        'jackets': jackets,
        'shirts': shirts,
        'bottoms': bottoms,
        'shoes': shoes
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

class ShowOutfitsView(CustomLoginRequiredMixin, ListView):
    '''Display all the clothing items.'''
    model = Outfit
    template_name = "project/show_outfits.html"

    context_object_name = "outfits"

    def get_queryset(self):
        '''Return only the clothing items belonging to the current user.'''
        return Outfit.objects.filter(user=self.request.user)  # Filter by user

