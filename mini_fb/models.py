'''
File: models.py
Description: Define data models for Facebook clone.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-02-16
Last Modified: 2025-02-16
'''
from django.db import models

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the data for each created profile.'''

    # Define data attributes for the Profile object
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)

    email = models.EmailField(blank=False)
    profile_img_url = models.URLField(blank=False)

