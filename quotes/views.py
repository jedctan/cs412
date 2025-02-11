from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Global vars

quotes = ["I feel like if you put something out into the universe, then you increase your chances of it happening.",
          "There was times when I was bullied about dancing and stuff. But you couldn't hit me hard enough to stop me from doing it.",
          "I feel like I've been playing Spider-Man my whole life. He's a character I've been pretending to be in my bedroom since I was a kid - so I've been preparing for this forever, I think."
          ]

images = ['quotes/tom1.jpg', 'quotes/tom2.jpg', 'quotes/tom3.jpg']

# Create your views here.

def quote(request):
    '''
    Define a view to handle the 'quote' request.
    '''
    rand_ind = random.randint(0,2)

    context = {
        "time": time.ctime(),
        "rand_quote": quotes[rand_ind],
        "rand_image": images[rand_ind]
    }
    template_name = 'quotes/quote.html'
    
    return render(request, template_name, context)
    

def show_all(request):
    '''
    Define a view to handle the 'show_all' request.
    '''
    context = {
        "time": time.ctime(),
        "quotes": quotes,
        "images": images
    }
    template_name = 'quotes/show_all.html'
    
    return render(request, template_name, context)
    

def about(request):
    '''
    Define a view to handle the 'about' request.
    '''
    context = {
        "time": time.ctime()
    }

    template_name = 'quotes/about.html'
    
    return render(request, template_name, context)
