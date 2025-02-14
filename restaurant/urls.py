'''
File: urls.py
Description: Defines URL patterns for the restaurant web app and maps URLs to corresponding view functions.
Author: Jed Tan
Email: jctan@bu.edu
Phone number: 919-619-1528
Year and major: Senior Computer Science
Date Created: 2025-02-11
Last Modified: 2025-02-14
'''

from django.urls import path
from django.conf import settings
from . import views

# URL patterns that are supported by this app:
urlpatterns = [ 
    path(r'', views.main, name="main_page"),
    path(r'main', views.main, name="main_page"),
    path(r'order', views.order, name="order"),
    path(r'confirmation', views.confirmation, name="confirmation"),

]
