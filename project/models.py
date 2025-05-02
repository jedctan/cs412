'''
File: models.py
Description: Define data models for the digital wardrobe app.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-04-13
'''

from django.db import models
from django.contrib.auth.models import User # for authentication
from django.urls import reverse # for URL redirection

# Create your models here.

class ClothingItem(models.Model):
    '''Encapsulate the data for each clothing item.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_file = models.ImageField(blank=False)


    # tuples: (in model, shown in forms)
    CATEGORY_CHOICES = [
        ('hat', 'Hat'),
        ('jacket', 'Jacket'),
        ('shirt', 'Shirt'),
        ('bottom', 'Bottom'),
        ('shoes', 'Shoes'),
    ]

    SEASON_CHOICES = [
        ('fall_winter', 'Fall/Winter'),
        ('spring_summer', 'Spring/Summer'),
        ('all_year', 'All Year'),
    ]

    # hat, jacket, shirt, bottom, or shoes
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=False)

    brand = models.TextField(blank=True)
    color = models.TextField(blank=True)
    season = models.CharField(max_length=20, choices=SEASON_CHOICES, blank=True)

    def __str__(self):
        '''Return a string representation of the clothing item.'''
        return f"{self.brand} {self.category}"


class Outfit(models.Model):
    '''Encapsulate the data for each outfit.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    event = models.ForeignKey('Event', null=True, blank=True, on_delete=models.SET_NULL)

    SEASON_CHOICES = [
        ('fall_winter', 'Fall/Winter'),
        ('spring_summer', 'Spring/Summer'),
        ('all_year', 'All Year'),
    ]

    OCCASION_CHOICES = [
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('party', 'Party'),
        ('work', 'Work'),
        ('vacation', 'Vacation'),
    ]

    season = models.CharField(max_length=20, choices=SEASON_CHOICES, blank=True, null=True)
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES, blank=True, null=True)

    # components of the outfit
    hat = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, related_name='outfits_hat')
    jacket = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, related_name='outfits_jacket')
    shirt = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, related_name='outfits_shirt')
    bottoms = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, related_name='outfits_bottoms')
    shoes = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, related_name='outfits_shoes')

    def __str__(self):
        '''Return a string representation of the outfit.'''
        return f"{self.name}"

class Event(models.Model):
    '''Encapsulate the data for events.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(blank=False)
    date = models.DateTimeField(blank=False)
    location = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        '''Return a string representation of the event.'''
        return f"{self.title}"


class RSVP(models.Model):
    '''Encapsulate the data for RSVPs to events.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')  # No duplicates

class Profile(models.Model):
    '''Encapsulate the data for each created profile.'''

    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    image_file = models.ImageField(blank=True) # profile pic not required
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='proj_profile')

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        '''Return a URL to display one instance of this object.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def add_friend(self, other):
        '''Adds a mutual friendship between self and other. Returns True if added, False otherwise.'''
        if self == other:
            return False  # can't friend yourself

        # check if the friendship already exists for either
        exists = Friendship.objects.filter(from_user=self, to_user=other).exists() or Friendship.objects.filter(from_user=other, to_user=self).exists()

        if exists:
            return False

        # create a friendship in both directions
        Friendship.objects.create(from_user=self, to_user=other, status=True)
        Friendship.objects.create(from_user=other, to_user=self, status=True)
        return True


class Friendship(models.Model):
    '''Encapsulate the data for friendships.'''
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    status = models.BooleanField(default=False) # True if accepted, False if not accepted
