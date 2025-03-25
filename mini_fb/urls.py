'''
File: urls.py
Description: Defines URL patterns for the Facebook web app and maps URLs to corresponding view functions.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-02-16
Last Modified: 2025-03-25
'''

from django.urls import path
from .views import *

# generic view for authentication / authorization
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ShowAllProfileViews.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view() , name="show_profile"),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('profile/<int:pk>/delete', DeleteStatusMessageView.as_view(), name="delete_status"),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name="update_status"),
    path('profile/<int:pk>/add_friend/<int:other_pk>', CreateFriendView.as_view(), name="add_friend"),
    path('profile/<int:pk>/friend_suggestions', ShowFriendSuggestionsView.as_view(), name="friend_suggestions"),
    path('profile/<int:pk>/news_feed', ShowNewsFeedView.as_view(), name="news_feed"),

    # authorization-related URLs
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_profiles'), name='logout'),
]
