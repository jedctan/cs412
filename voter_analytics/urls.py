'''
File: urls.py
Description: Defines URL patterns for the Voter Analytics app and maps URLs to corresponding view functions.
Author: Jed Tan
Email: jctan@bu.edu
Date Created: 2025-04-03
'''

from django.urls import path
from . import views 

urlpatterns = [
    # map the URL (empty string) to the view
	path(r'', views.VotersListView.as_view(), name='home'),
    path(r'voters', views.VotersListView.as_view(), name='voter_list'),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
    path('graphs/', views.VoterGraphView.as_view(), name='graphs'),
    
]
