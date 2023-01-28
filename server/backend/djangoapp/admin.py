from django.contrib import admin
# from .models import related models
from .models import User, CarMake, CarModel, CarPurchase, Customer


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email']
    search_fields = ['username', 'first_name', 'last_name', 'email']


# CarModelInline class
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 5


# CarModelAdmin class
@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year', 'type', 'car_make']
    search_fields = ['name', 'car_make', 'year']
    list_filter = ['type']


# CarMakeAdmin class with CarModelInline
@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [
        CarModelInline,
    ]
    list_display = ['id', 'name']
    search_fields = ['name']


# CarPurchaseAdmin
@admin.register(CarPurchase)
class CarPurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'purchase_date', 'dealer_id']
    list_filter = ['dealer_id', 'purchase_date']


# CustomerAdmin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name", "email", "phone"]