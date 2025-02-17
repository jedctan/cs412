'''
File: urls.py
Description: Defines URL patterns for the Facebook web app and maps URLs to corresponding view functions.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-02-16
Last Modified: 2025-02-16
'''

from django.urls import path
from .views import ShowAllProfileViews, ShowProfilePageView # our view class definition 

urlpatterns = [
    path('', ShowAllProfileViews.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view() , name="show_profile")

]
