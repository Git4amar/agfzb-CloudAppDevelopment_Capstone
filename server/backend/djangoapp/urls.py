from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path('about', views.about, name='about_us'),

    # path for contact us view
    path('contact', views.contact, name='contact_us'),

    # path for registration
    path('register', views.register_dealership_user, name='registration'),

    # path for login
    path('login', views.login_dealership_user, name='login'),

    # path for logout
    path('logout', views.logout_dealership_user, name='logout'),

    path('', views.get_dealerships, name='index'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path('dealer/<int:dealer_id>/<str:dealer_name>/review', views.add_review, name='add_review'),

    # path for React review form API
    path('details/<int:dealer_id>/', views.review_form_details, name='details_review_form'),

] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)