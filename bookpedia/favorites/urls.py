from django.urls import path


# MY IMPORTS
from . import views


# Application namespace 
app_name = 'favorites'


urlpatterns = [
    path('add/<slug:slug>', views.add_book, name='add-book'),
    path('remove/<slug:slug>', views.remove_book, name='remove-book'),    
]

