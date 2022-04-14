import imp
from django.urls import path

from . import views


#Application Namespace

app_name= 'home'

#Url Patterns

urlpatterns = [
    path('', views.home, name='index'),
]

