"""ORM Models for djangoapp"""
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """User Model"""

    pass


class CarMake(models.Model):
    """Car-Make Model"""

    name = models.CharField(max_length=90)
    description = models.TextField()

    def __str__(self):
        return f"Car Make: {self.name}"

    def natural_key(self):
        return self.name


class CarModel(models.Model):
    """Car-Model Model"""

    car_make = models.ForeignKey(
        CarMake, on_delete=models.CASCADE, related_name="car_make_models"
    )
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=90)
    type_choices = [("sedan", "Sedan"), ("suv", "SUV"), ("wagon", "WAGON")]
    type = models.CharField(max_length=6, choices=type_choices)
    year = models.DateField()

    def __str__(self):
        return f"Model: {self.name}, Make: {self.car_make}"


class Customer(models.Model):
    """Customer Model"""

    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class CarPurchase(models.Model):
    """Car Purchase Model"""

    purchase_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="customer_purchases"
    )
    dealer_id = models.IntegerField()
    car_model = models.ForeignKey(
        CarModel, on_delete=models.PROTECT, related_name="car_model_purchases"
    )

    def __str__(self):
        return f"Customer: {self.customer}, Model: {self.car_model}, Dealer: {self.dealership}, Purchase Date: {self.purchase_date}"


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    """Model Class-only for Car Dealer"""

    def __init__(
        self, address, city, full_name, id, lat, long, short_name, st, state, zip
    ):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        self.state = state
        # Dealer zip
        self.zip = zip

    @classmethod
    def from_dict(cls, document):
        """Class Method to create Dealer"""
        kwargs = {}
        valid_args = [
            "address",
            "city",
            "full_name",
            "id",
            "lat",
            "long",
            "short_name",
            "st",
            "state",
            "zip",
        ]
        for key in document:
            if key in valid_args:
                kwargs[key] = document[key]

        return cls(**kwargs)

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    """Model Class-only for Reviews"""

    def __init__(
        self,
        dealership,
        name,
        purchase,
        review,
        sentiment=None,
        purchase_date=None,
        car_make=None,
        car_model=None,
        car_year=None,
    ):
        self.sentiment = sentiment
        self.car_year = car_year
        self.car_model = car_model
        self.car_make = car_make
        self.purchase_date = purchase_date
        self.review = review
        self.purchase = purchase
        self.name = name
        self.dealership = dealership

    @classmethod
    def from_dict(cls, document):
        """Class Method to create Review"""
        kwargs = {}
        valid_args = [
            "dealership",
            "name",
            "purchase",
            "review",
            "sentiment",
            "purchase_date",
            "car_make",
            "car_model",
            "car_year",
        ]
        for key in document:
            if key in valid_args:
                kwargs[key] = document[key]

        return cls(**kwargs)

    def __str__(self):
        return f"Review for {self.dealership} by {self.name}"
