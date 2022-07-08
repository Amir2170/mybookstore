from django.urls import path

# MY IMPORTS
from . import views


# App name
app_name = 'review'


urlpatterns = [
    path('<slug:book_slug>/', views.rate_book, name='rate'),
]
