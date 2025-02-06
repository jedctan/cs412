from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.

def home(request):
    '''
    Define a view to handle the 'home' request.
    '''
    context = {
        "time": time.ctime(),
        "r_num": chr(random.randint(65,98)),
    }
    template_name = 'quotes/home.html'
    
    return render(request, template_name, context)

def quote(request):
    '''
    Define a view to handle the 'home' request.
    '''

    response_text = '''
    <html>
    <h1>ni jiao shenme</h1>

    </html>
    '''
    
    return HttpResponse(response_text)
    

def show_all(request):
    '''
    Define a view to handle the 'home' request.
    '''

    response_text = '''
    <html>
    <h1>Hello, world!</h1>

    </html>
    '''
    
    return HttpResponse(response_text)
    

def about(request):
    '''
    Define a view to handle the 'home' request.
    '''

    response_text = '''
    <html>
    <h1>Hello, world!</h1>

    </html>
    '''
    
    return HttpResponse(response_text)
    
