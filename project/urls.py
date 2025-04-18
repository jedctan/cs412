from django.urls import path
from django.conf import settings
# generic view for authentication / authorization
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [ 
    path('', ShowWardrobeView.as_view(), name="show_wardrobe"),
    path('add_item', CreateClothingItemView.as_view(), name="create_clothing_item"),
    path('outfit/', create_outfit, name='custom_create_outfit'),
    path('outfits/', ShowOutfitsView.as_view(), name='outfit_list'),
    # authorization-related URLs
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='project-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='project-logout'),

]