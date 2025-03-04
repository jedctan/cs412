'''
File: urls.py
Description: Defines URL patterns for the Facebook web app and maps URLs to corresponding view functions.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-02-16
Last Modified: 2025-03-02
'''

from django.urls import path
from .views import *

urlpatterns = [
    path('', ShowAllProfileViews.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view() , name="show_profile"),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('profile/<int:pk>/delete', DeleteStatusMessageView.as_view(), name="delete_status"),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name="update_status"),

]
