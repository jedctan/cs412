'''
File: models.py
Description: Define data models for Facebook web app.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-02-16
Last Modified: 2025-03-04
'''
from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the data for each created profile.'''

    # Define data attributes for the Profile object
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    # profile_img_url = models.URLField(blank=False)
    image_file = models.ImageField(blank=True) # profile pic not required

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        '''Return a URL to display one instance of this object.'''
        # utilize reverse function to look up URL for show_profile and index using primary key to get the correct URL
        return reverse('show_profile', kwargs={'pk': self.pk})

    def get_status_messages(self):
        '''Return a QuerySet of status messages for this profile'''
        # use object manager to retrieve status messages
        # match the foreign key of profile to self (instance of type Profile) and order by the timestamp
        status_messages = StatusMessage.objects.filter(profile=self).order_by('timestamp')
        return status_messages
    
class StatusMessage(models.Model):
    '''Encapsulate the data for each created status message.'''

    # automatically set the field to now everytime the object is saved
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)

    # foreign key: in this project we have a one to many relationship from profiles to status messages
    # because each profile can have many status messages while each status message is associated with at most one profile
    # cascade delete: if a profile is deleted all status messages associated with it are deleted as well
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this status message.'''
        return f'{self.message}'
    
    def get_images(self):
        '''Return all images associated with this status message.'''
        status_images = StatusImage.objects.filter(status_message=self)  # Get all StatusImage objects
        return [si.image for si in status_images]
        


class Image(models.Model):
    '''Encapsulates the image file.'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    # optional caption field
    caption = models.TextField(blank=True)

class StatusImage(models.Model):
    '''Encapsulates the relationship between images that are associated with a Profile and StatusMessage.'''
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
