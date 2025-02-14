"""
File: views.py
Description: Handles the restaurant website views, including order processing and confirmation.
Author: Jed Tan
Email: jctan@bu.edu
Phone number: 919-619-1528
Year and major: Senior Computer Science
Date Created: 2025-02-11
Last Modified: 2025-02-14
"""


from django.shortcuts import render # render function used to render HTML templates
import time # time module used to generate timestamps for footer and order completion time
import random # random module used to randomly select daily special and time to completion


def main(request):
    '''Function to show the main page of the website to describe the restaurant.'''
    template_name = "restaurant/main.html" # template that contains the main page HTML file
    context = {
        "time": time.ctime(), # time needed for the footer time generated component
    } 
    return render(request, template_name, context) # renders the HTML file using the HTTP request and the specified template


def order(request):
    '''Function that responds to the user's get request to show the web page with the form.'''

    template_name = "restaurant/order.html" # template that contains the order HTML file


    # randomly choose the daily special from a list of sauces
    random_choice = random.randint(0,3)
    daily_special_list = ["Mystery", "Soy", "Habanero", "Onion"]

    # daily special item that is supplied at run time
    context = {
        "daily_special" : daily_special_list[random_choice],
        "time": time.ctime(),
    }

    return render(request, template_name, context) # renders the HTML file using the HTTP request and the specified template

def confirmation(request):
    '''Function to handle a form submission and generate a result.'''

    template_name = "restaurant/confirmation.html" # template that contains the order HTML file

    # read the form data into python variables:
    # first check if the post request exists
    if request.POST: 

        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        special_instructions = request.POST["special_instructions"]

        # determine time when order is ready, between 30-60 minutes from current time
        current_time = time.time() # current time in seconds
        random_period = random.randint(30,60) * 60 # random 30-60 minute period in seconds
        readytime = time.ctime(current_time + random_period) # add times and format into readable form

        # lists of what the user ordered that will be passed to the HTML template to be displayed in the confirmation screen
        nuggets = []
        sauces = []

        # price accumulator
        price = 0 

        # check what type of nuggets the user ordered and add the price of each to the total price
        if "nugget4" in request.POST:
            nuggets.append("4 Piece Nugget - $5")
            price += 5
        if "nugget8" in request.POST:
            nuggets.append("8 Piece Nugget - $10")
            price += 10
        if "nugget100" in request.POST:
            nuggets.append("100 Piece Nugget - $50")
            price += 50
        if "nugget2000" in request.POST:
            nuggets.append("2000 Piece Nugget - $1000")
            price += 1000
        
        # check what type of sauces the user ordered and add the price of each to the total price
        if "honeymustard" in request.POST:
            sauces.append("Honey Mustard")
            price += 5
        if "ketchup" in request.POST:
            sauces.append("Ketchup")
            price += 5
        if "bbq" in request.POST:
            sauces.append("BBQ")
            price += 5
        if "ranch" in request.POST:
            sauces.append("Ranch")
            price += 1000
        if "dailyspecial" in request.POST:
            sauces.append(request.POST["dailyspecial"] + " Sauce")
            price += 5000


        context = {
            "name": name,
            "phone": phone,
            "email": email,
            "special_instructions": special_instructions,
            "nuggets": nuggets,
            "sauces": sauces,
            "readytime": readytime,
            "price": price,
            "time": time.ctime(),
        }

    return render(request, template_name, context=context) # renders the HTML file using the HTTP request and the specified template


