from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
)


# My imports
from accounts.forms import CustomUserCreationForm



def auth_forms(request):
    return {
        'login_form': AuthenticationForm(),
        'user_creation_form': CustomUserCreationForm(),
        'user_change_form': UserChangeForm(),
    }
