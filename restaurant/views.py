from django.shortcuts import render

# Create your views here.

def main(request):
    '''Function to show the main page of the website to describe the restaurant.'''
    template_name = "restaurant/main.html" # template that contains the main page HTML file
    return render(request, template_name) # renders the HTML file using the HTTP request and the specified template


def order(request):
    '''Function that responds to the user's get request to show the web page with the form.'''

    template_name = "restaurant/order.html" # template that contains the order HTML file
    return render(request, template_name) # renders the HTML file using the HTTP request and the specified template

def confirmation(request):
    '''Function to handle a form submission and generate a result.'''

    template_name = "restaurant/confirmation.html" # template that contains teh order HTML file

    # read the form data into python variables:
    # first check if the post request exists
    if request.POST: 

        name = request.POST['name']
        favorite_color = request.POST['favorite_color']

        context = {
            'name': name,
            'favorite_color':  favorite_color,
            
        }

    return render(request, template_name, context=context)


