import imp
from django.urls import path

# MY IMPORTS
from . import views


#Application Namespace

app_name= 'home'

#Url Patterns

urlpatterns = [
    path('', views.home, name='index'),
    path('books/<slug:slug>/', views.book_detail, name='book-detail'),
]

