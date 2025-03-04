'''
File: forms.py
Description: Defines forms for creating and managing Profile and StatusMessage objects in the database.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-03-02
Last Modified: 2025-03-02
'''

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database.'''

    class Meta:
        '''Associate this form with the Profile model from our database'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image_file']


class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a StatusMessage for a Profile to the database.'''

    class Meta:
        '''Associate this form with the StatusMessage model from our database.'''
        model = StatusMessage
        fields = ['message']