from django.urls import path
from .views import ShowAllProfileViews # our view class definition 

urlpatterns = [
    path('', ShowAllProfileViews.as_view(), name="show_all_profiles")
]
