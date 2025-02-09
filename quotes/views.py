from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Global vars

quotes = []
images = []

# Create your views here.

# def home(request):
#     '''
#     Define a view to handle the 'home' request.
#     '''
#     context = {
#         "time": time.ctime(),
#         "r_num": chr(random.randint(65,98)),
#     }
#     template_name = 'quotes/home.html'
    
#     return render(request, template_name, context)

def quote(request):
    '''
    Define a view to handle the 'quote' request.
    '''

    context = {
        "time": time.ctime(),
        "r_num": chr(random.randint(65,98)),
    }
    template_name = 'quotes/quote.html'
    
    return render(request, template_name, context)
    

def show_all(request):
    '''
    Define a view to handle the 'show_all' request.
    '''

    template_name = 'quotes/show_all.html'
    
    return render(request, template_name)
    

def about(request):
    '''
    Define a view to handle the 'about' request.
    '''
    template_name = 'quotes/about.html'
    
    return render(request, template_name)
