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
    ]

    # hat, jacket, shirt, bottom, or shoes
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=False)

    brand = models.TextField(blank=True)
    color = models.TextField(blank=True)
    season = models.CharField(max_length=20, choices=SEASON_CHOICES, blank=True)

    def __str__(self):
        return f"{self.brand} {self.category}"


class Outfit(models.Model):
    '''Encapsulate the data for each outfit.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    # components of the outfit
    hat = models.ForeignKey('project.ClothingItem', on_delete=models.SET_NULL, null=True, related_name='outfits_hat')
    jacket = models.ForeignKey('project.ClothingItem', on_delete=models.SET_NULL, null=True, related_name='outfits_jacket')
    shirt = models.ForeignKey('project.ClothingItem', on_delete=models.SET_NULL, null=True, related_name='outfits_shirt')
    bottoms = models.ForeignKey('project.ClothingItem', on_delete=models.SET_NULL, null=True, related_name='outfits_bottoms')
    shoes = models.ForeignKey('project.ClothingItem', on_delete=models.SET_NULL, null=True, related_name='outfits_shoes')


class Event(models.Model):
    '''Encapsulate the data for events.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(blank=False)
    date = models.DateTimeField(blank=False)
    outfit = models.ForeignKey('project.Outfit', on_delete=models.SET_NULL, null=True)
    location = models.TextField(blank=True)

class Friendship(models.Model):
    '''Encapsulate the data for friendships.'''
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    status = models.BooleanField(default=False) # True if accepted, False if not accepted