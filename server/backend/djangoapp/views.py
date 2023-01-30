"""views for djangoapp"""
import os
import logging
import jsonpickle

from django.shortcuts import render
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dotenv import load_dotenv

from .forms import RegistrationForm
from .restapis import (
    get_dealers_from_cloudant,
    get_dealer_reviews_from_cloudant,
    post_review,
)
from .models import CarModel



load_dotenv()

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, "djangoapp/about.html")


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, "djangoapp/contact.html")


# Create a `login_request` view to handle sign in request
def login_dealership_user(request):
    if request.method == "POST":
        username = request.POST["login_username"]
        password = request.POST["login_password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back {user.first_name}!")
        else:
            messages.error(request, "Invalid username / password")

        return redirect("djangoapp:index")


# Create a `logout_request` view to handle sign out request
def logout_dealership_user(request):
    logout(request)
    return redirect("djangoapp:index")


# ...


# Create a `registration_request` view to handle sign up request
def register_dealership_user(request):
    if request.method == "GET":
        context = {"registration_form": RegistrationForm()}

    else:
        new_user_registration_form = RegistrationForm(request.POST)
        if new_user_registration_form.is_valid():
            new_user = new_user_registration_form.save(commit=False)
            new_user.set_password(new_user.password)
            new_user.first_name = new_user.first_name.capitalize()
            new_user.last_name = new_user.last_name.capitalize()
            new_user.save()
            login(request, new_user)
            messages.success(
                request,
                f"Welcome {new_user.first_name}!, You've successfully registered",
            )
            return redirect("djangoapp:index")
        else:
            context = {"registration_form": new_user_registration_form}

    return render(request, "djangoapp/registration.html", context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        # Get dealers from the URL
        context["dealerships"] = get_dealers_from_cloudant(os.environ["FN_DEALERS_URL"])
        return render(request, "djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        # Get reviews for the dealer
        context["dealership_reviews"] = get_dealer_reviews_from_cloudant(
            os.environ["FN_REVIEWS_URL"], dealerId=dealer_id
        )
        context["dealership_details"] = get_dealers_from_cloudant(
            os.environ["FN_DEALERS_URL"], dealerId=dealer_id
        )[0]
        return render(request, "djangoapp/dealer_details.html", context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
@login_required
def add_review(request, dealer_id, dealer_name):
    context = {"dealer_id": dealer_id, "dealer_name": dealer_name}
    if request.method == "POST":
        review = jsonpickle.decode(request.body)
        result = {}
        if review["car_purchased"]:
            result["error_car"] = True if review["car"] == "default" else False
            result["error_purchase_date"] = (
                True if review["purchase_date"] == "" else False
            )
            if not result["error_car"]:
                try:
                    purchased_car = CarModel.objects.get(pk=review["car"])
                except CarModel.DoesNotExist:
                    result["error_car"] = True
                else:
                    pass

        result["error_content"] = True if review["content"] == "" else False

        if True not in result.values():
            review_to_post = {
                "name": f"{request.user.first_name} {request.user.last_name}",
                "dealership": dealer_id,
                "review": review["content"],
                "purchase": review["car_purchased"],
                "purchase_date": review["purchase_date"]
                if review["car_purchased"]
                else None,
                "car_make": purchased_car.car_make.name
                if review["car_purchased"]
                else None,
                "car_model": purchased_car.name if review["car_purchased"] else None,
                "car_year": purchased_car.year.strftime("%Y")
                if review["car_purchased"]
                else None,
            }
            post_review(os.environ["FN_POST_REVIEW_URL"], review=review_to_post)
            messages.success(request, "Review has been posted successfully!")

        status_code = 400 if True in result.values() else 200
        return JsonResponse({"result": result}, status=status_code)
    else:
        return render(request, "djangoapp/add_review.html", context)


def review_form_details(request, dealer_id):
    cars = serialize("json", CarModel.objects.all(), use_natural_foreign_keys=True)
    return JsonResponse({"cars": cars}, status=200)


#def csrf_failure(request, reason="TO DEBUG"):
#    return JsonResponse(
#        {
#            "headers": jsonpickle.decode(
#                jsonpickle.encode(request.headers, unpicklable=False)
#            ),
#            "reason": reason,
#        }
#    )
