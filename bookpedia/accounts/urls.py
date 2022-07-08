from django.urls import path
from django.contrib.auth import views as auth_views

# MY IMPORTS
from . import views


# Aplication name
app_name = 'accounts'


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create-account/', views.user_creation, name='user-creation'),
    path('change_account/', views.user_change, name='user-change'),
]
