'''
File: models.py
Description: Define data models for Facebook web app.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-02-16
Last Modified: 2025-03-21
'''
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User # for authentication

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    
    
    def get_friends(self):
        '''Return a list of all the friends for this profile.'''

        # get all of the friends objects that have this profile in either profile1 or profile2
        friends1 = Friend.objects.filter(profile1=self)
        friends2 = Friend.objects.filter(profile2=self)

        result_list = []

        # for all friend relationships where this profile is in profile1, retrieve profile2
        for i in friends1:
            result_list.append(i.profile2)
        
        # for all friend relationships where this profile is in profile2, retrieve profile1
        for j in friends2:
            result_list.append(j.profile1)
        
        return result_list
    
    def add_friend(self, other):
        '''Adds a friend relation for two profiles: self and other.'''
        # test if this friend relation exists for profile1 + profile2 or profile2 + profile1
        if self == other:
            return False
    
        profile1_matches = Friend.objects.filter(profile1=self, profile2=other)
        profile2_matches = Friend.objects.filter(profile1=other, profile2=self)

        if profile1_matches or profile2_matches:
            return False
        else:
            Friend.objects.create(profile1=self, profile2=other)
            return True

    def get_friend_suggestions(self):
        '''Return a list of Friend suggestions for this Profile.'''

        # find all profiles that are not in this Profile's friend list
        all_profiles = Profile.objects.all() # QuerySet of all existing profiles
        current_friends = self.get_friends() # list of profile objects
        res = []

        for p in all_profiles:
            if p not in current_friends and p != self:
                res.append(p)
        
        return res

    def get_news_feed(self):
        '''Return list of all StatusMessages for this Profile and all of its Friends.'''
        
        # List of friends of this profile
        friends_list = Profile.get_friends(self)

        # Add current profile to this list
        friends_list.append(self)

        # Filter through all status messages, based on if the profile is in this list
        res = StatusMessage.objects.filter(profile__in=friends_list).order_by('-timestamp')

        return res

    
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
    
    def get_absolute_url(self):
        '''Return a URL to display one instance of this object.'''
        # utilize reverse function to look up URL for show_profile and index using primary key to get the correct URL
        return reverse('show_profile', kwargs={'pk': self.profile.pk})

    def get_images(self):
        '''Return all images associated with this status message.'''
        status_images = StatusImage.objects.filter(status_message=self)  # Get all StatusImage objects
        return [si.image for si in status_images] # Return just the Image objects
        

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


class Friend(models.Model):
    '''Encapsulates the idea of an edge connecting two nodes within the social network.'''
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this friend relationship.'''
        return f'{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}'
