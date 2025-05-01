'''
File: urls.py
Description: Define urls for the digital wardrobe app.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-04-13
'''

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [ 
    path('', ShowWardrobeView.as_view(), name="show_wardrobe"),
    path('add_item', CreateClothingItemView.as_view(), name="create_clothing_item"),
    path('create_outfit/', create_outfit, name= "custom_create_outfit"),
    path('outfits/', ShowOutfitsView.as_view(), name="outfit_list"),
    path('item/<int:pk>/', ShowClothingItemDetail.as_view(), name="item_detail"),
    path('outfit/<int:pk>/', ShowOutfitDetail.as_view(), name="outfit_detail"),
    path('update_item/<int:pk>/', UpdateClothingItemView.as_view(), name="update_clothing_item"),
    path('outfit/<int:pk>/edit_custom/', edit_outfit_custom, name="custom_update_outfit"),
    path('item/<int:pk>/delete/', DeleteClothingItemView.as_view(), name="delete_clothing_item"),
    path('outfit/<int:pk>/delete/', DeleteOutfitView.as_view(), name="delete_outfit"),

    # events-related URLs
    path('events/create/', EventCreateView.as_view(), name='create_event'),
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/rsvp/', RSVPCreateView.as_view(), name='rsvp_event'),

    # profile-related URLs
    path('register/', CreateProfileView.as_view(), name='project_create_profile'),
    path("profile/<int:pk>/", ShowProfileView.as_view(), name="project_show_profile"),
    path("profile/<int:pk>/update/", UpdateProfileView.as_view(), name="project_update_profile"),
    # authorization-related URLs
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name="project_login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name="project_logout"),

]