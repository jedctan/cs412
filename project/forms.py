'''
File: forms.py
Description: Defines forms for creating and managing user created objects.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-04-14
'''

from django import forms
from .models import ClothingItem, Outfit

class CreateClothingItem(forms.ModelForm):
    '''Form to create a clothing item.'''

    class Meta:
        model = ClothingItem
        fields = ['image_file', 'category', 'brand', 'color', 'season']


    
