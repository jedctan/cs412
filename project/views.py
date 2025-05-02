'''
File: views.py
Description: Define views for the digital wardrobe app.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-04-13
'''
from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from .models import ClothingItem
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *

from django.shortcuts import render, redirect
from .models import *

from django.contrib.auth.mixins import LoginRequiredMixin # for authentication    
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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
        event_id = request.POST.get('event')
        season = request.POST.get('season')
        occasion = request.POST.get('occasion')

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
        event = Event.objects.filter(id=event_id).first() if event_id else None

        # create the outfit with the selected clothing items
        Outfit.objects.create(
            user=request.user,
            name=name,
            notes=notes,
            hat=hat,
            jacket=jacket,
            shirt=shirt,
            bottoms=bottoms,
            shoes=shoes,
            event=event,
            season=season,
            occasion=occasion,
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

    # get events the user RSVPed to, but hasn't used in any outfit yet
    assigned_event_ids = Outfit.objects.filter(user=request.user, event__isnull=False).values_list('event_id', flat=True)
    rsvp_events = Event.objects.filter(rsvp__user=request.user).exclude(id__in=assigned_event_ids)

    # loads template, adds all of the clothing items, returns the response
    return render(request, 'project/create_outfit_custom.html', {
        'hats': hats,
        'jackets': jackets,
        'shirts': shirts,
        'bottoms': bottoms,
        'shoes': shoes,
        'rsvp_events': rsvp_events,
        'seasons': Outfit.SEASON_CHOICES,
        'occasions': Outfit.OCCASION_CHOICES,
    })


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
        event_id = request.POST.get('event')

        # update the outfit's clothing items based on the selected IDs
        outfit.hat = ClothingItem.objects.filter(id=hat_id).first() if hat_id else None
        outfit.jacket = ClothingItem.objects.filter(id=jacket_id).first() if jacket_id else None
        outfit.shirt = ClothingItem.objects.filter(id=shirt_id).first() if shirt_id else None
        outfit.bottoms = ClothingItem.objects.filter(id=bottoms_id).first() if bottoms_id else None
        outfit.shoes = ClothingItem.objects.filter(id=shoes_id).first() if shoes_id else None
        outfit.event = Event.objects.filter(id=event_id).first() if event_id else None
        
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

    # get all RSVP events for the user
    assigned_event_ids = Outfit.objects.filter(user=request.user, event__isnull=False).exclude(pk=outfit.pk).values_list('event_id', flat=True)
    rsvp_events = Event.objects.filter(rsvp__user=request.user).exclude(id__in=assigned_event_ids)

    # loads template, adds the outfit and all of the clothing items, returns the response
    return render(request, 'project/update_outfit_custom.html', {
        'outfit': outfit,
        'hats': hats,
        'jackets': jackets,
        'shirts': shirts,
        'bottoms': bottoms,
        'shoes': shoes,
        'rsvp_events': rsvp_events,
    })

class CustomLoginRequiredMixin(LoginRequiredMixin):
    '''Custom class to add changes to the LoginRequiredMixin class.'''

    def get_login_url(self):
        '''Return the URL for this app's login page.'''
        # sends us to login screen if we try to create a profile when not logged in
        return reverse('project_login')

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
    
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'project/create_event.html'
    
    def get_success_url(self):
        return reverse('event_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'project/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        my_profile = self.request.user.proj_profile
        friend_ids = Friendship.objects.filter(
            from_user=my_profile
        ).values_list('to_user__user__id', flat=True)

        # all events where the user is either the current user or a friend
        return Event.objects.filter(
            models.Q(user__id__in=friend_ids) | models.Q(user=self.request.user)).order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rsvp_ids = RSVP.objects.filter(user=self.request.user).values_list('event_id', flat=True)
        context['rsvped_event_ids'] = set(rsvp_ids)
        return context


class EventDetailView(DetailView):
    '''Display the details of an event.'''
    model = Event
    template_name = 'project/event_detail.html'
    context_object_name = 'event'

    # get outfit for this user for this event
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        current_user = self.request.user

        # current user outfit
        user_outfit = Outfit.objects.filter(user=current_user, event=event).first()
        context['user_outfit'] = user_outfit

        # get all RSVPed users except the one currently viewing the page
        rsvped_users = User.objects.filter(rsvp__event=event).exclude(id=current_user.id).distinct()

        # map RSVPed users to their outfit
        outfits_by_user = {
            user: Outfit.objects.filter(user=user, event=event).first()
            for user in rsvped_users
        }
        context['rsvp_outfits'] = outfits_by_user

        return context

    
class CreateProfileView(CreateView):
    '''
    A combined user + profile creation view. 
    1. Displays UserCreationForm and CreateProfileForm.
    2. Processes both on POST, logs in user, then redirects.
    '''
    model = Profile
    form_class = CreateProfileForm
    template_name = "project/create_profile_form.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # if the user put in an invalid password, we need to show the user creation form again
        if 'user_form' not in context:

            # add the user creation form to the context
            context["user_form"] = UserCreationForm()

        return context

    def form_valid(self, form):
        '''This method handles the form submission and saves the new object to the Django db. '''

        # recontruct the user creation form
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            # save the new user to db
            user = user_form.save()

            # log the user in
            login(self.request, user)
            
            # attach the user to the profile
            form.instance.user = user

            return super().form_valid(form)
        else:
            # add the invalid form to the context and re-render the page
            # this is so we can see errors from bad password input
            return self.render_to_response(self.get_context_data(
                form=form,
                user_form=user_form
            ))

    def get_success_url(self):
        return reverse("show_wardrobe")

class ShowProfileView(LoginRequiredMixin, DetailView):
    '''View to display a user's profile.'''
    model = Profile
    template_name = "project/show_profile.html"
    context_object_name = "profile"

class UpdateProfileView(CustomLoginRequiredMixin, UpdateView):
    '''View to update a user's profile.'''
    model = Profile
    form_class = CreateProfileForm
    template_name = "project/update_profile_form.html"
    context_object_name = "profile"

    def get_queryset(self):
        '''Ensure users can only update their own profile.'''
        return Profile.objects.filter(user=self.request.user)

    def get_success_url(self):
        '''Return the URL to redirect to after updating the profile.'''
        return reverse('project_show_profile', kwargs={'pk': self.object.pk})

class ProfileDirectoryView(CustomLoginRequiredMixin, ListView):
    '''View to display a directory of all profiles except the current user.'''
    model = Profile
    template_name = "project/profile_directory_view.html"
    context_object_name = "profiles"

    # returns all profiles except the current user's profile
    def get_queryset(self):
        return Profile.objects.exclude(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get the current user's profile
        my_profile = self.request.user.proj_profile

        # find all friendships where the user's profiles pk is present, then get the ids of the friends then get the PKs of those
        friends_ids = Profile.objects.filter(pk__in=Friendship.objects.filter(from_user=my_profile).values_list('to_user', flat=True)).values_list('pk', flat=True)

        # convert to Python set for dupes
        context['friends_ids'] = set(friends_ids)
        return context

class CreateFriendView(CustomLoginRequiredMixin, View):
    '''View class to handle the creation of Friend relations.'''

    def get_object(self):
        '''Returns Profile corresponding to the signed in user.'''
        profiles = Profile.objects.filter(user=self.request.user)
        # since admin is associated with multiple profiles, we will return the first no matter what
        return profiles[0]

    def dispatch(self, request, *args, **kwargs):
        ''''Set up friendship creation.'''
        
        # from the request get the 2 primary keys
        pk1 = self.get_object().pk
        pk2 = self.kwargs['other_pk']

        profile1 = Profile.objects.get(pk=pk1)
        profile2 = Profile.objects.get(pk=pk2)

        profile1.add_friend(profile2)
        
        return redirect(reverse('project_show_profile', kwargs={'pk': profile2.pk}))

class ToggleRSVPView(CustomLoginRequiredMixin, View):
    '''View to toggle RSVP status for an event.'''
    
    def post(self, request, *args, **kwargs):
        '''Post since we are always changing the state of the RSVP.'''
        # get event with pk
        event = Event.objects.get(pk=kwargs['pk'])

        # check if RSVP exists
        rsvp = RSVP.objects.filter(user=request.user, event=event).first()

        if rsvp:
            # Clear outfit.event link
            Outfit.objects.filter(user=request.user, event=event).update(event=None)

            # Delete the RSVP
            rsvp.delete()
        else:
            # if no rsvp exists, create one
            RSVP.objects.create(user=request.user, event=event)

        return redirect('event_list')

