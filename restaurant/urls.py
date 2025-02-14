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
