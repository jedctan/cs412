'''
File: forms.py
Description: Defines forms for creating and managing user created objects.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-04-14
'''

from django import forms
from .models import *

from django.forms import DateTimeInput

class CreateClothingItemForm(forms.ModelForm):
    '''Form to create a clothing item.'''

    class Meta:
        model = ClothingItem
        fields = ['image_file', 'category', 'brand', 'color', 'season']

class UpdateClothingItemForm(forms.ModelForm):
    '''Form to update a clothing item.'''

    class Meta:
        model = ClothingItem
        fields = ['image_file', 'category', 'brand', 'color', 'season']


class EventForm(forms.ModelForm):
    '''Form to create or update an event.'''

    class Meta:
        model = Event
        fields = ['title', 'date', 'location', 'description']

        # create custom widget for date field to allow datetime input
        widgets = {
            'date': DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            )
        }

        # needed for editing existing events to ensure the date format is correct
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['date'].input_formats = ['%Y-%m-%dT%H:%M']

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database.'''

    class Meta:
        '''Associate this form with the Profile model from our database'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image_file']


